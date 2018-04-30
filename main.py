#!/usr/bin/env python3
import os
import utils
import speech_recognition as sr
import numpy as np
import xmlrpc.client
import snowboydecoder
import signal
from numpy import linalg as LA
from utils import cosineSim, euclideanDist
from nltk.tokenize.stanford import StanfordTokenizer

# Configuration
BASE_SNLP_PATH = os.path.abspath("./stanford-postagger")
SNLP_TAGGER_JAR = os.path.join(BASE_SNLP_PATH, "stanford-postagger.jar")
STT_API = 'google'
COMMANDS = {
	'time':		['What is the time', 'Tell me the time'],
	'date':		['What is the date', 'Tell me the date'],
	'ls':		['List directory', 'List files and folders'],
	'rm':		['Delete file'],
	'rmdir':	['Delete directory', 'Delete folder'],
	'Kill Berry': ['Kill berry', 'Strangle berry', 'Destroy berry', 'Please kill berry']
}

# Connect to sent2vec server
sent2vec = xmlrpc.client.ServerProxy('http://localhost:8123')
def sentenceToVector(sentence):
	return np.asarray(sent2vec.embed_sentence(utils.tokenize(tknzr, sentence)))

# Tokenizer
tknzr = StanfordTokenizer(SNLP_TAGGER_JAR, encoding='utf-8')

# Preprocess sentences
sentenceToCommand = []
for command, sentences in COMMANDS.items():
	for sentence in sentences:
		sentenceToCommand.append((sentence, command))

senteceVectorToCommand = []
for sentence, command in sentenceToCommand:
	sentenceVector = sentenceToVector(sentence)
	senteceVectorToCommand.append((sentenceVector, command))

# Main functions
interrupted = False
def signal_handler(signal, frame):
    global interrupted
    interrupted = True
def interrupt_check():
    global interrupted
    return interrupted

def closestCommandEuclidean(inputVector):
	closestDist = float('Inf')
	closestCommand = None
	for sentenceVector, command in senteceVectorToCommand:
		dist = euclideanDist(inputVector, sentenceVector)
		if dist < closestDist:
			closestDist = dist
			closestCommand = command

	return closestCommand, closestDist
def closestCommandCosine(inputVector):
	maxSimilarity = 0.0
	closestCommand = None
	for sentenceVector, command in senteceVectorToCommand:
		sim = cosineSim(inputVector, sentenceVector)
		if sim > maxSimilarity:
			maxSimilarity = sim
			closestCommand = command

	return closestCommand, maxSimilarity

def listenForCommand():
	# Obtain audio from microphone
	with sr.Microphone() as source:
		snowboydecoder.play_audio_file()
		print("Listening...")
		audio = r.listen(source)
		print("Converting speech to text")

	try:
		# Recognize speech
		if STT_API == 'google':
			text = r.recognize_google(audio) #r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")
		elif STT_API == 'sphinx':
			text = r.recognize_sphinx(audio)

		# Recognize command
		print("Speech to text: {}".format(text))
		textVector = sentenceToVector(text)
		print("Closest command (using euclidean distance): {}".format(closestCommandEuclidean(textVector)))
		print("Closest command (using cosine similarity): {}".format(closestCommandCosine(textVector)))
	except sr.UnknownValueError:
		print("Could not understand audio")
	except sr.RequestError as e:
		print("Request Error: {}".format(e))

	print()

# Initialize recognizer
r = sr.Recognizer()
r.dynamic_energy_threshold = True

# Initial energy adjustment
with sr.Microphone() as source:
	r.adjust_for_ambient_noise(source, duration=1)

detector = snowboydecoder.HotwordDetector("models/snowboy.umdl", sensitivity=0.5)
signal.signal(signal.SIGINT, signal_handler)

# Start listening
print("Waiting for hotword")
detector.start(detected_callback=listenForCommand, interrupt_check=interrupt_check, sleep_time=0.03)
detector.terminate()
