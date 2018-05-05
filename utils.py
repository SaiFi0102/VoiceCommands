import os, re, io
import numpy as np
import numpy.linalg as LA
import pydub
import speech_recognition as sr
from pydub.playback import play
from gtts import gTTS
from gtts.tts import gTTSError
from time import sleep
from nltk.tokenize.stanford import StanfordTokenizer

playDing = False
interrupted = False

dingAudio = pydub.AudioSegment.from_wav("resources/ding.wav")
errorAudio = pydub.AudioSegment.from_mp3("resources/error.mp3")
networkErrorAudio = pydub.AudioSegment.from_mp3("resources/networkError.mp3")
notUnderstoodAudio = pydub.AudioSegment.from_mp3("resources/notUnderstood.mp3")

recognizer = None

BASE_SNLP_PATH = os.path.abspath("./stanford-postagger")
SNLP_TAGGER_JAR = os.path.join(BASE_SNLP_PATH, "stanford-postagger.jar")
tknzr = StanfordTokenizer(SNLP_TAGGER_JAR, encoding='utf-8')

def signal_handler(signal, frame):
	global interrupted
	interrupted = True
def interrupt_check():
	global interrupted
	return interrupted

def initSpeechRecognizer():
	global recognizer
	# Initialize recognizer
	recognizer = sr.Recognizer()
	recognizer.dynamic_energy_threshold = True

	# Initial energy adjustment
	with sr.Microphone() as source:
		recognizer.adjust_for_ambient_noise(source, duration=1)

def listenForSpeech():
	global playDing
	# Obtain audio from microphone
	with sr.Microphone() as source:
		playDing = True
		print("Listening...")
		audio = recognizer.listen(source)
		print("Converting speech to text")

	try:
		text = recognizer.recognize_google(audio)
		return text
	except sr.UnknownValueError as e:
		print("Could not understand audio")
		playNotUnderstoodSpeech()
		raise e
	except sr.RequestError as e:
		print("Request Error: {}".format(e))
		playNetworkErrorSpeech()
		raise e

def pollForSound():
	global playDing
	while True:
		if interrupt_check():
			return
		if playDing:
			play(dingAudio)
			playDing = False
		sleep(0.05)

def playTextToSpeech(text):
	try:
		tts = gTTS(text, 'en')
		mp3Data = io.BytesIO()
		tts.write_to_fp(mp3Data)
		mp3Data.seek(0)

		audio = pydub.AudioSegment.from_mp3(mp3Data)
		play(audio)
	except gTTSError as e:
		playErrorSpeech()

def playNetworkErrorSpeech():
	play(networkErrorAudio)

def playErrorSpeech():
	play(errorAudio)

def playNotUnderstoodSpeech():
	play(notUnderstoodAudio)

def tokenize(sentence, to_lower=True):
	"""Arguments:
		- sentence: a string to be tokenized
		- to_lower: lowercasing or not
	"""
	sentence = sentence.strip()
	sentence = ' '.join([format_token(x) for x in tknzr.tokenize(sentence)])
	if to_lower:
		sentence = sentence.lower()
	sentence = re.sub('((www\.[^\s]+)|(https?://[^\s]+)|(http?://[^\s]+))','<url>',sentence) #replace urls by <url>
	sentence = re.sub('(\@ [^\s]+)','<user>',sentence) #replace @user268 by <user>
	filter(lambda word: ' ' not in word, sentence)
	return sentence

def format_token(token):
	""""""
	if token == '-LRB-':
		token = '('
	elif token == '-RRB-':
		token = ')'
	elif token == '-RSB-':
		token = ']'
	elif token == '-LSB-':
		token = '['
	elif token == '-LCB-':
		token = '{'
	elif token == '-RCB-':
		token = '}'
	return token

def tokenize_sentences(tknzr, sentences, to_lower=True):
	"""Arguments:
		- tknzr: a tokenizer implementing the NLTK tokenizer interface
		- sentences: a list of sentenceentences
		- to_lower: lowercasing or not
	"""
	return [tokenize(tknzr, s, to_lower) for s in sentences]

def cosineSim(u, v):
	return np.dot(u, v)/(LA.norm(u)*LA.norm(v))
def euclideanDist(u, v):
	return LA.norm(u-v)

if __name__ == "__main__":
	print("Test text to speech")
	while True:
		text = input("Text: ")
		playTextToSpeech(text)