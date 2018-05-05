# VoiceCommands
A python program to run voice commands using speech-to-text, text-to-speech, and sent2vec for sentence comparison

# Prerequisites

## Libraries
- ffmpeg

## Python Libraries
- Numpy https://pypi.org/project/numpy/
- NLTK https://pypi.org/project/nltk/
- PyAudio https://pypi.org/project/PyAudio/
- SpeechRecognition https://pypi.org/project/SpeechRecognition/
- gTTS https://pypi.org/project/gTTS/
- pydub https://pypi.org/project/pydub/
- sent2vec https://github.com/epfml/sent2vec

## Getting libraries
```shell
sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg
sudo pip3 install numpy pyaudio nltk gTTS pydub SpeechRecognition

git clone https://github.com/epfml/sent2vec
cd sent2vec
make
cd src
pip3 install .
```

## Files
- Download and extract folder ./stanford-postagger from https://nlp.stanford.edu/software/tagger.shtml
- Download and extract models/wiki-unigrams.bin (or any other sent2vec model file) from pretrained model links on https://github.com/epfml/sent2vec/blob/master/README.md

# Instructions
- Run sent2vecServer.py
- Make sure server's IP is correct in main.py (sent2vec = xmlrpc.client.ServerProxy('http://localhost:8123'))
- Run main.py
