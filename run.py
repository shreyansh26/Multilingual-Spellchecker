import spellchecker
import argparse

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    CRED = '\033[91m'
    CWHITE  = '\33[37m'


parser = argparse.ArgumentParser()
parser.add_argument("--distance", help="Specify the Levenshtein distance")
parser.add_argument("--lang", help="Specify the language => [es - Spanish], [de - German], [fr - French], [pt - Portugese]")
parser.add_argument("--load", help="Load external data file")
parser.add_argument("--predict", help="Give possible alternatives of the incorrect word")
args = parser.parse_args()

distance = args.distance
language = args.lang
load = args.load
predict = args.predict

if distance is None:
	distance = 2
if language is None:
	language = 'en'
if predict is not None:
	predict = 1

if load == 'hi':
	spell = spellchecker.SpellChecker(distance=distance)
	spell.word_frequency.load_text_file('./resources/hi.txt')
else:
	spell = spellchecker.SpellChecker(language=language, distance=distance)

while 1:
	print(">>", end=' ')
	s = input()
	if s == 'quit':
		print("Bye!")
		break
	s = s.split()
	misspelled = spell.unknown(s)
	correct = s.copy()
	# print(misspelled)
	a = []
	ind = []
	for w in misspelled:
		indices = [i for i, x in enumerate(s) if x == w]
		for i in indices:
			a.append((w, i))
			ind.append(i)

	print(bcolors.HEADER + "Original: " + bcolors.ENDC, end = ' ')
	for i, word in enumerate(s):
		if i not in ind:
			print(bcolors.CWHITE + word + bcolors.ENDC, end = ' ')
		else:
			print(bcolors.CRED + word + bcolors.ENDC, end = ' ')

	print()

	if predict == 1:
		print()
		for i, word in enumerate(s):
			if (word, i) in a:
				print(bcolors.OKGREEN + word + ": " + bcolors.CRED + ' '.join(list(spell.candidates(word))) + bcolors.ENDC,)

		print()

	print(bcolors.HEADER + "Corrected: " + bcolors.ENDC, end = ' ')
	# for word, ind in a:
	# 	correct[ind] = spell.correction(word)
	for i, word in enumerate(s):
		if (word, i) in a:
			print(bcolors.OKGREEN + spell.correction(word) + bcolors.ENDC, end = ' ')
		else:
			print(bcolors.CWHITE + word + bcolors.ENDC, end = ' ')

	print()