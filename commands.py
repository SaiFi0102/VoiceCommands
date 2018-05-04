def testCommand(text):
	print("Callback test, text: " + text)

SENTENCES = {
	'time':		['What is the time', 'Tell me the time'],
	'date':		['What is the date', 'Tell me the date'],
	'ls':		['List directory', 'List files and folders'],
	'rm':		['Delete file'],
	'rmdir':	['Delete directory', 'Delete folder'],
	'Kill Berry': ['Kill berry', 'Strangle berry', 'Destroy berry', 'Please kill berry']
}
CALLBACKS = {
	'time':		testCommand,
	'date':		testCommand,
	'ls':		testCommand,
	'rm':		testCommand,
	'rmdir':	testCommand
}