import os
import re
import numpy as np
import numpy.linalg as LA
import snowboydecoder
from time import sleep

playDing = False
interrupted = False

def signal_handler(signal, frame):
	global interrupted
	interrupted = True
def interrupt_check():
	global interrupted
	return interrupted

def pollForSound():
	global playDing
	global interrupted
	while True:
		if interrupt_check():
			return
		if playDing:
			snowboydecoder.play_audio_file()
			playDing = False
		sleep(0.05)

def tokenize(tknzr, sentence, to_lower=True):
	"""Arguments:
		- tknzr: a tokenizer implementing the NLTK tokenizer interface
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