# VoiceCommands
A python program to run voice commands using speech-to-text, text-to-speech, and sent2vec for sentence comparison

# Prerequisites

## Python Libraries
- Numpy
- NTLK
- SpeechRecognition https://pypi.org/project/SpeechRecognition/
- PyAudio https://gist.github.com/diegopacheco/d5d4507988eff995da297344751b095e#file-pyaudio-ubuntu-install-md
- sent2vec https://github.com/epfml/sent2vec

## Files
- Download and extract folder ./stanford-postagger from https://nlp.stanford.edu/software/tagger.shtml
- Download and extract models/wiki-unigrams.bin (or any other sent2vec model file) from pretrained model links on https://github.com/epfml/sent2vec/blob/master/README.md

# Instructions
- Run sent2vecServer.py
- Make sure server's IP is correct in main.py (sent2vec = xmlrpc.client.ServerProxy('http://localhost:8123'))
- Run main.py
