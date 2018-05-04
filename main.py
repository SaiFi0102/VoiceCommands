#!/usr/bin/env python3
import os
import utils
import speech_recognition as sr
import numpy as np
import xmlrpc.client
import snowboydecoder
import signal
import threading
import commands
from numpy import linalg as LA
from utils import cosineSim, euclideanDist
from nltk.tokenize.stanford import StanfordTokenizer

# Configuration
DING_SOUND_FILE = "resources/ding.wav"
BASE_SNLP_PATH = os.path.abspath("./stanford-postagger")
SNLP_TAGGER_JAR = os.path.join(BASE_SNLP_PATH, "stanford-postagger.jar")
STT_API = 'google'

# Connect to sent2vec server
sent2vec = xmlrpc.client.ServerProxy('http://localhost:8123')
def sentenceToVector(sentence):
	raw = np.asarray(sent2vec.embed_sentence(utils.tokenize(tknzr, sentence)))
	return raw/LA.norm(raw)

# Tokenizer
tknzr = StanfordTokenizer(SNLP_TAGGER_JAR, encoding='utf-8')

# Preprocess sentences
sentenceToCommand = []
for command, sentences in commands.SENTENCES.items():
	for sentence in sentences:
		sentenceToCommand.append((sentence, command))

senteceVectorToCommand = []
for sentence, command in sentenceToCommand:
	sentenceVector = sentenceToVector(sentence)
	senteceVectorToCommand.append((sentenceVector, command))

# Main functions
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
		utils.playDing = True
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
		closestCommand = closestCommandCosine(textVector)
		closestCommand2 = closestCommandEuclidean(textVector)
		print("Closest command (using cosine similarity): {}".format(closestCommand))
		print("Closest command (using euclidean distance): {}".format(closestCommand2))
		commands.CALLBACKS[closestCommand[0]](text)
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

# Sound player thread
soundThread = threading.Thread(target=utils.pollForSound)
soundThread.start()

# Start listening
signal.signal(signal.SIGINT, utils.signal_handler)
detector = snowboydecoder.HotwordDetector("models/snowboy.umdl", sensitivity=0.5)
print("Waiting for hotword")
detector.start(detected_callback=listenForCommand, interrupt_check=utils.interrupt_check, sleep_time=0.03)
detector.terminate()
