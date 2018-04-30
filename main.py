#!/usr/bin/env python3
import os
import utils
import speech_recognition as sr
import numpy as np
import xmlrpc.client
from numpy import linalg as LA
from utils import cosineSim, euclideanDist
from nltk.tokenize.stanford import StanfordTokenizer

# Configuration
BASE_SNLP_PATH = os.path.abspath("./stanford-postagger")
SNLP_TAGGER_JAR = os.path.join(BASE_SNLP_PATH, "stanford-postagger.jar")
STT_API = 'google'
COMMANDS = {
	'time':		['What is the time'],
	'date':		['What is the date'],
	'ls':		['List directory'],
	'rm':		['Delete file'],
	'rmdir':	['Delete directory']
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
def closestCommandEuclidean(inputVector):
	closestDist = float('Inf')
	closestCommand = None
	for sentenceVector, command in senteceVectorToCommand:
		dist = euclideanDist(inputVector, sentenceVector)
		if dist < closestDist:
			closestDist = dist
			closestCommand = command

	return closestCommand
def closestCommandCosine(inputVector):
	maxSimilarity = 0.0
	closestCommand = None
	for sentenceVector, command in senteceVectorToCommand:
		sim = cosineSim(inputVector, sentenceVector)
		if sim > maxSimilarity:
			maxSimilarity = sim
			closestCommand = command

	return closestCommand

r = sr.Recognizer()
while True:
	# Obtain audio from microphone
	with sr.Microphone() as source:
		r.adjust_for_ambient_noise(source)
		print("Say something!")
		audio = r.listen(source) # consider using Snowboy
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
