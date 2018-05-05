#!/usr/bin/env python3
import os
import utils
import numpy as np
import xmlrpc.client
import snowboydecoder
import signal
import threading
import commands
from numpy import linalg as LA
from utils import cosineSim, euclideanDist

# Connect to sent2vec server
sent2vec = xmlrpc.client.ServerProxy('http://localhost:8123')
def sentenceToVector(sentence):
	raw = np.asarray(sent2vec.embed_sentence(utils.tokenize(sentence)))
	return raw/LA.norm(raw)

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
	try:
		text = utils.listenForSpeech()

		# Recognize command
		print("Speech to text: {}".format(text))
		textVector = sentenceToVector(text)
		closestCommand = closestCommandCosine(textVector)
		closestCommand2 = closestCommandEuclidean(textVector)
		print("Closest command (using cosine similarity): {}".format(closestCommand))
		print("Closest command (using euclidean distance): {}".format(closestCommand2))
		commands.CALLBACKS[closestCommand[0]](text)
	except Exception:
		pass
	print()

# Initialize speech recognizer
utils.initSpeechRecognizer()

# Sound player thread
soundThread = threading.Thread(target=utils.pollForSound)
soundThread.start()

# Start listening
signal.signal(signal.SIGINT, utils.signal_handler)
detector = snowboydecoder.HotwordDetector("models/snowboy.umdl", sensitivity=0.5)
print("Waiting for hotword")
detector.start(detected_callback=listenForCommand, interrupt_check=utils.interrupt_check, sleep_time=0.03)
detector.terminate()
