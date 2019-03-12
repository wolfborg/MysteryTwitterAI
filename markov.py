# Mystery Twitter AI - markov.py
# Derek Chaplin

# Overall goal: A Twitter bot which will generate tweets by forming sentences using mystery novel text files as its reference data.

# Markov Chains
# InitialState * Probabilites = NextState

# Need tweepy installed if you want to 

import random, time, sys, os

# Uncomment for Twitter posting
import tweepy
from keys import *
#
# Also must have a file keys.py which has the following API info:
#	CONSUMER_KEY
#	CONSUMER_SECRET
#	ACCESS_KEY
#	ACCESS_SECRET
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Imports the list of bad words for the bot to ignore
def importBadWords():
	f = open('badwords.txt', 'r')
	result = []
	for line in f:
		result.append(line)
	return result

# Reads the text files within a given directory
def processData(foldername):
	result = []
	for file in os.listdir(foldername):
		if file.endswith(".txt"):
			result.extend(processNovel(os.path.join(foldername, file)))
	return result

# Adds each word to a big list of words from every processed novel
def processNovel(filename):
	f = open(filename, 'r')
	result = []	
	for line in f:
		words = line.split(' ')
		for word in words:
			# Removes newlines, tabs, and fixes quotes and apostrophes
			word = word.strip('\n')
			word = word.strip('\t')
			word = word.replace('\xe2\x80\x98', "'")
			word = word.replace('\xe2\x80\x99', "'")
			word = word.replace('\xe2\x80\x9d', "")
			word = word.replace('\xe2\x80\x9c', "")
			word = word.replace('_', "")
			word = word.replace('(', "")
			word = word.replace(')', "")
			word = word.replace('"', "")
			result.append(word)
	return result

# Returns [] of beginners and {} of ngrams
def markovChainWords(txt, ngramCount):
	ngrams = {}
	beginners = []
	count = 0
	badwords = importBadWords()
	endingpunctuations = ['.', '!', '?']
	abbreviations = ['Mr.','Mrs.','Dr.','A.M.','P.M.']
	# Creates the ngrams dictionary
	for word in txt:
		if word in badwords:
			continue

		# If the count doesn't go over the number of words
		if count < len(txt)-ngramCount:
			# If we don't have the word already
			if word not in ngrams:
				# Add it to the dictionary
				ngrams[word] = []
			# Append to key the next ngrams
			nextngram = ""
			for i in range(1,ngramCount):
				nextngram += (txt[count+i])
				if i != ngramCount-1:
					nextngram += " "
			ngrams[word].append(nextngram)
			if word.istitle() and word[-1] not in endingpunctuations:
				beginners.append(word)
		count += 1

	return [ngrams, beginners]

# Returns the resulting Markov chain string
def textChain(ngrams, beginners, charLimit):
	endingpunctuations = ['.', '!', '?']
	abbreviations = ['Mr.','Mrs.','Dr.','A.M.','P.M.']

	current = random.choice(beginners)
	result = current
	# Runs until the last word has an ending punctuation.
	while result[-1] not in endingpunctuations:
		next = random.choice(ngrams[current])
		if len(result + " " + next) > charLimit:
			words = result.split(' ')
			if result[-1] in endingpunctuations and words[-1] not in abbreviations:
				return result
			current = random.choice(beginners)
			result = current
			next = random.choice(ngrams[current])
		result += " " + next
		current = next.split(' ')
		current = current[-1]

	words = result.split(' ')
	if words[-1] in abbreviations:
		result = textChain(ngrams, beginners, charLimit)

	return result

# Processes all the novels in the cleaned folder
txt = processData("mystery-novels\cleaned")

# Defaults to generate one trigram with a 140 caracter limit
ngramCount = 3
charLimit = 140
trials = 1

# Gets the number of arguments recieved
args = len(sys.argv)
# First argument sets the number of ngrams to use
if args > 1:
	ngramCount = int(sys.argv[1])
# Second argument sets the character limit to use for the generated text
if args > 2:
	charLimit = int(sys.argv[2])
# Third argument sets the number of trials
if args > 3:
	trials = int(sys.argv[3])

# Creates the Markov chain dictionary
ngrams, beginners = markovChainWords(txt, ngramCount)

# Comment this out if you're running the Twitter bot
# Runs for the number of trials specified
#for i in range(trials):
	# Generate and print the text
	#print textChain(ngrams, beginners, charLimit)

# Uncomment this to post results to Twitter
while True:
	## Runs the text generator chain and prints the tweet
 	text = textChain(ngrams, beginners, charLimit)
 	api.update_status(text)
 	time.sleep(600)#Tweet every 10 minutes
	
