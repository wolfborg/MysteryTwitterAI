# Mystery Twitter AI - markov.py

# Overall goal: A Twitter bot which will generate tweets by forming sentences using mystery novel text files as its reference data.
# First goal: Generate sentences with a Markov chain

# Markov Chains
# InitialState * Probabilites = NextState

#############################################################################################
# UPDATE 3/21/17
# Currently:
#	1. Converts a text file into a list of words.
#	2. Create a dictionary of ngrams, holds the frequency of following words.
#	3. Also collects a list of words that start sentences.
# 	4. Generates a string <= 140 characters using a random beginning word and a
#		 random next word based on the ngrams dictionary.
#
# To-Do:
#	Allow variable amount of ngrams to be looked at.
#	Prevent open/close quote confusions.
#	End sentence at a period but don't end for Dr., Mr., so on.
#	Bad word filter so I don't accidentally end up expelled.
#	Integrate Twitter API to post tweets every x amount of time.
#############################################################################################

import random

# Parameters: filename - a txt file in the "mystery-novels" directory
def processNovel(filename):
	f = open("mystery-novels/" + filename, 'r')
	result = []
	
	for line in f:
		words = line.split(' ')
		for word in words:
			# Removes newlines, tabs, and fixes quotes and apostrophes
			word = word.strip('\n')
			word = word.strip('\t')
			word = word.replace('\xe2\x80\x99', "'")
			word = word.replace('\xe2\x80\x9d', '"')
			word = word.replace('\xe2\x80\x9c', '"')
			result.append(word)
	return result

# Parameters: txt - a list of words to use for data
def textChain(txt):
	ngrams = {}
	beginners = []
	count = 0

	# Creates the ngrams dictionary
	for word in txt:
		if count < len(txt)-1:
			if word not in ngrams:
				ngrams[word] = []
			ngrams[word].append(txt[count+1])
			if word.istitle():
				beginners.append(word)
		count += 1

	current = random.choice(beginners)
	result = current

	# Runs until the next word exceeds 140 characters
	# To-Do: Change this so it ends at a word with a period.
	# Possible To-Do: More than once sentence?
	while True:
		next = random.choice(ngrams[current])
		if len(result + " " + next) > 140:
			break
		result += " " + next
		current = next

	#print ngrams
	return result

# Small example text to reference: The Gettysburg Address
#txt = '''Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battle-field of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. But, in a larger sense, we can not dedicate -- we can not consecrate -- we can not hallow -- this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, nor long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated here to the unfinished work which they who fought here have thus far so nobly advanced. It is rather for us to be here dedicated to the great task remaining before us -- that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion -- that we here highly resolve that these dead shall not have died in vain -- that this nation, under God, shall have a new birth of freedom -- and that government of the people, by the people, for the people, shall not perish from the earth.'''

# Big example text to reference: After Dark
txt = processNovel("after-dark.txt")

# Runs the text generator chain and prints the tweet
print textChain(txt)
	
