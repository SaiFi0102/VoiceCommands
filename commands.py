import utils
from datetime import datetime
from datetime import date
import subprocess
from glob import glob
import os
import webbrowser


def testCommand(text):
	print("Callback test, text: " + text)

def timeCommand(text):
	output = datetime.now().strftime("It's %I:%M %p")
	utils.playTextToSpeech(output)

def dateCommand(text):
	output = datetime.now().strftime("Today is %A, %d %B, %Y") # google strftime to know which to use for day, dateok anything else 
	utils.playTextToSpeech(output)

def deleteFilecommand(text):
	file=False
	text1=text.split()
	print(text1)
	string=''
	for p,i in enumerate(text1):
		
		if i=="delete":
			file=True
			continue
		if file == True:
			file = False
			string=i
	paths = glob('/home/r2d2/*/{}'.format(string))
	paths=str(paths)
	paths=paths.replace("[",'')
	paths=paths.replace("]",'')
	paths=paths.replace("'",'')
	print(paths)
	if(len(paths)!=0):
		os.remove(paths)
		utils.playTextToSpeech("requested file deleted")
	else:
		utils.playTextToSpeech("requested file does not exist")


def deleteDircommand(text):
	string = text.split()
	dir=''
	file=False
	for p,i in enumerate(string):
		if i=="directory":
			file=True
			continue
		if file == True:
			file = False
			dir=i
	subprocess.call("/home/r2d2/qwert/deleteDir.sh {}".format(dir),shell=True)

def copyFilecommand(text):
	t=text.split()
	arg1=''
	arg2=''
	flag1 = False
	flag2 = False
	for i,j in enumerate(t):
		if j == 'copy':
			flag1=True
			continue
		if flag1 == True:
			flag1=False
			arg1 = j
		if j == 'to':
			flag2=True
			continue
		if flag2 == True:
			flag2=False
			arg2 = j
	finalarg=arg1 + ' ' + arg2
	print(finalarg)
	subprocess.call("/home/r2d2/qwert/copyFile.sh {}".format(finalarg),shell=True)

def moveFilecommand(text):
	t=text.split()
	arg1=''
	arg2=''
	flag1 = False
	flag2 = False
	for i,j in enumerate(t):
		if j == 'copy':
			flag1=True
			continue
		if flag1 == True:
			flag1=False
			arg1 = j
		if j == 'to':
			flag2=True
			continue
		if flag2 == True:
			flag2=False
			arg2 = j
	finalarg=arg1 + ' ' + arg2
	print(finalarg)
	subprocess.call("/home/r2d2/qwert/moveFile.sh {}".format(finalarg),shell=True)


def openAppCommand(text):

	string=text.replace('open','')
	string=string.replace('.com','')
	finalstr='http://'
	finalstr=finalstr+string+'.com'
	webbrowser.open(finalstr)





SENTENCES = {
	'time':		['What is the time', 'Tell me the time'],
	'date':		['What is the date', 'Tell me the date',"date", "day"],
	'ls':		['List directory', 'List files and folders'],
	'rm':		['Delete file'],
	'cp':		['copy file to directory'],
	'rmdir':	['Delete directory', 'Delete folder'],
	'mv':		['move file to directory'],
	'open':		['open app']

}
CALLBACKS = {
	'time':		timeCommand,
	'date':		dateCommand,
	'cd':		copyFilecommand,
	'ls':		testCommand,
	'rm':		deleteFilecommand,
	'rmdir':	deleteDircommand,
	'mv':       moveFilecommand,
	'open':		openAppCommand
}

if __name__ == '__main__':
	openAppCommand("youtube.com")
