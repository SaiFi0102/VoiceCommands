from datetime import datetime
from datetime import date


def testCommand(text):
    print("Callback test, text: " + text)


def timeCommand(text):
    output = datetime.now().strftime("It's %I:%M %p")
    utils.playTextToSpeech(output)


def dateCommand(text):
    output = datetime.now().strftime(
        "Today is %A, %d %B, %Y")  # google strftime to know which to use for day, dateok anything else
    utils.playTextToSpeech(output)


def listCommand(text):


def deleteCommand(text):
    subprocess.call("delte.sh", shell=True)


SENTENCES = {
    'time': ['What is the time', 'Tell me the time'],
    'date': ['What is the date', 'Tell me the date', "date", "day"],
    'ls': ['List directory', 'List files and folders'],
    'rm': ['Delete file'],
    'rmdir': ['Delete directory', 'Delete folder']
}
CALLBACKS = {
    'time': timeCommand,
    'date': dateCommand,
    'ls': testCommand,
    'rm': testCommand,
    'rmdir': testCommand
}

if __name__ == '__main__':
    dateCommand("")
