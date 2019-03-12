To run this program, simple enter "python markov.py".
By default, it will generate a string which is a maximum of 140 characters using an n-gram of three.
You can specify up to three options to produce different results.
	options: ngramCount  charLimit  trials

For example: python markov.py 2 250 3
That will produce three text generations each made using a bigram and a max character limit of 250

If you want it to work as a Twitter bot, you have to uncomment certain sections of the code (which are labeled) and also make a keys.py file with the four keys needed to use the Twitter API.