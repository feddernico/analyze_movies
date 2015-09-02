#!/usr/bin/python3

import csv
import os
import sys

## Functions:
# adds a rating for a given movie inside a given movie dictionary.
def addMovieRate( movieDict, key, rating ):
	# if the movie is not yet inside the dictionary, it's added with
	# the current rating as ratingSum; 1 as rateUsers; rating as Avg.
	if movieDict.get(key) == None:
		movieDict[key] = [ rating, 1, rating ]
	# otherwise it updates ratingSum, rateUsers, and the average rating for 
	# the current movie.
	else:
		ratingSum = (movieDict[key][0] + rating)
		rateUsers = (movieDict[key][1] + 1)
		movieDict[key] = [ ratingSum, rateUsers, ratingSum/rateUsers ]    					
	return

# calculates the maximum available indexes and returns them as a list.
def calcMaxIndex( dictList ):
	maxIndexes = []
	for dic in dictList:
		# if the number of required movies is greater than the number of movies 
		# available then all movies are returned. Finally the maximum index for 
		# each group is calculated.
		maxIndexes.append( (len(dic) - 1) if int(sys.argv[2]) > len(dic) else int(sys.argv[2]) )
	return maxIndexes

# prints out a table using those given variables:
# dic - the dictionary that contains the data
# groupKey - the movie keys that identifies each movie to display
# title - the title of the table
def printTable( dic, groupKey, title ):
	# prints out the title of the given dictionary
	print( '\n%s Best Movies:\n' % title )

	# finds what is the max title length
	maxTitleLen = -1
	for key in groupKey:
		if len(movieDict[key][0]) > maxTitleLen:
			maxTitleLen = len(movieDict[key][0])

	# prints the table header
	print('{rank:{rankLen}s} {title:{titleLen}s} {rat:s} {vot:s}'.format( 
			rank = 'Ranking', title = 'Movie', rat = 'Rating', vot = 'Votes', 
					rankLen = 7, titleLen = maxTitleLen ))

	# prints the dividing lines between header and data
	print('{rank:{rankLen}s} {title:{titleLen}s} {ratVot:s}'.format( 
		rank = '-------', title = '-'*maxTitleLen, ratVot = '------ -----', 
				rankLen = 7, titleLen = maxTitleLen ))

	# prints the table data
	for i, key in enumerate(groupKey, start = 1):
		print('{position:7d} {title:{titleLen}s} {rating:3.2f} {votes:7d}'
			.format( position = i, title = movieDict[key][0], 
				rating = round(dic[key][2], 2), votes = dic[key][1], 
				titleLen = maxTitleLen ))


## Script:
# the first argument is always the called script, so the number of given 
# arguments must be exactly 3:
if len(sys.argv) == 3:
	# analyzes the arguments of the script:
	# 1. if the first argument is not gender or agegroup or age
	#    then something went wrong with the first argument.
	try:
		assert sys.argv[1] in ('gender', 'age', 'agegroup')
	except AssertionError:
		sys.exit('The first argument is not valid.')

	
	# 2. if the first argument is OK, then the second must be an integer.
	try:
		int(sys.argv[2])
	except ValueError:
		sys.exit('The second argument is not an integer.')
	
	# finds out what is the current data directory.
	datDir = os.path.dirname(os.path.realpath(__file__)) + '/data'

	# opens the ratings dataset and creates the dictionary for that data.
	with open(datDir + '/ratings.dat', 'rt', encoding = 'latin_1') as ratings:
		r = csv.reader( (line.replace('::', '\\') for line in ratings), delimiter = '\\', quotechar = '"')
		# the key of the ratingDict is a multiple key composed by UserID and MovieID
		ratingDict = { (row[0], row[1]): row[ 2: ]  for row in r }

	# opens the users dataset and creates the dictionary for that data.
	with open(datDir + '/users.dat', 'rt', encoding = 'latin_1') as users:
		r = csv.reader( (line.replace('::', '\\') for line in users), delimiter = '\\', quotechar = '"')
		# the key of the usersDict is the UserID
		usersDict = { row[0]: row[ 1: ]  for row in r }

	# opens the movies dataset and creates the dictionary for that data.
	with open(datDir + '/movies.dat', 'rt', encoding = 'latin_1') as movies:
		r = csv.reader( (line.replace('::', '\\') for line in movies), delimiter = '\\', quotechar = '"')
		# the key of the movieDict is MovieID.
		movieDict = { row[0]: row[ 1: ]  for row in r }	

	# if the user selected the gender grouping variable
	if sys.argv[1] == 'gender':

		# sets correctly the group values, the group value position inside the user dictionary,
		# the groups description and the groups data
		groupValues = ['M', 'F']
		groupValuePos = 0
		groupDesc = ['Male', 'Female']
		groups = [{} for _ in range(len(groupValues))]

	# if the user selected the age grouping variable
	elif( sys.argv[1] == 'agegroup' or sys.argv[1] == 'age' ):

		# sets correctly the group values, the group value position inside the user dictionary,
		# the groups description and the groups data
		groupValues = ['1', '18', '25', '35', '45', '50', '56']
		groupValuePos = 1
		groupDesc = ['Under 18', '18-24', '25-34', '35-44', '45-49', '50-55', '56+']
		groups = [{} for _ in range(len(groupValues))]

	# loops over the rating dictionary.
	for key, val in ratingDict.items():
		# gets the current rating and converts it to an integer value.
		rating = int(ratingDict[(key[0], key[1])][0])

		# for each age group inside the usersDict adds the correct movie rating		
		for i, val in enumerate(groupValues, start = 0):
			if usersDict[key[0]][groupValuePos] == val:
				addMovieRate(groups[i], key[1], rating)
	
	# calculates the dictionary maximum index available per gender group
	maxIndexes = calcMaxIndex(groups)

	# returns the first n keys of the best rated movies for each age group.
	# When movies have the same rating, they are ordered by number of votes received
	moviesKey = [[] for _ in range( len(groupValues) )]
	for i, val in enumerate(groups, start = 0):
		moviesKey[i] = sorted(val.keys(), key=lambda x: (val[x][2], val[x][1]), reverse = True)[0:maxIndexes[i]]

	# prints out the ranking splitted by age group. The report is composed by:
	# 1) Ranking
	# 2) Movie - The movie title
	# 3) Avg Rating - The average rating
	# 4) Votes - The number of votes received by the movie
	for i in range( len(groupValues) ):
		printTable(groups[i], moviesKey[i], groupDesc[i])
		
# if the arguments given in input are not 3 the script will stop.
else:
	sys.exit('You haven\'t provided the correct number of arguments (2)')