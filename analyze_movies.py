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
	print('{rank:{rankLen}s}  {title:{titleLen}s} {rat:s} {vot:s}'.format( 
			rank = 'Ranking', title = 'Movie', rat = 'Rating', vot = 'Votes', 
					rankLen = 7, titleLen = maxTitleLen ))

	# prints the dividing lines between header and data
	print('{rank:{rankLen}s}  {title:{titleLen}s} {ratVot:s}'.format( 
		rank = '-------', title = '-'*maxTitleLen, ratVot = '------ -----', 
				rankLen = 7, titleLen = maxTitleLen ))

	# prints the table data
	for i, key in enumerate(groupKey, start = 1):
		print('{position:7d}  {title:{titleLen}s} {rating:3.2f} {votes:7d}'
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
		# creates two movie dictionaries - one per gender - that has MovieID as key and as variables:
		# 0) The sum of ratings;
		# 1) The number of users that rated that movie;
		# 2) The average calculated as: sum_of_ratings/num_users_rated.
		maleMovies = {}
		femaleMovies = {}

		# loops over the rating dictionary.
		for key, val in ratingDict.items():
			# gets the current rating and converts it to an integer value.
			rating = int(ratingDict[(key[0], key[1])][0])

			# if the user is a Male
			if usersDict[key[0]][0] == 'M':
				addMovieRate(maleMovies, key[1], rating)
			# else, if the user is a Female
			else:
				addMovieRate(femaleMovies, key[1], rating)

		# calculates the dictionary maximum index available per gender group
		maxIndexes = calcMaxIndex([maleMovies, femaleMovies])

		# returns the first n keys of the best rated movies for males and females.
		# When movies have the same rating, they are ordered by number of votes received
		maleMovieKey = sorted(maleMovies.keys(), key=lambda x: (maleMovies[x][2], maleMovies[x][1]), reverse=True)[0:maxIndexes[0]]
		femaleMovieKey = sorted(femaleMovies.keys(), key=lambda x: (femaleMovies[x][2], femaleMovies[x][1]), reverse=True)[0:maxIndexes[1]]

		# prints out the ranking splitted by gender. The report is composed by:
		# 1) Ranking
		# 2) Movie - The movie title
		# 3) Avg Rating - The average rating
		# 4) Votes - The number of votes received by the movie
		printTable( maleMovies, maleMovieKey, 'Male' )
		printTable( femaleMovies, femaleMovieKey, 'Female' )


	# if the user selected the age grouping variable
	elif( sys.argv[1] == 'agegroup' or sys.argv[1] == 'age' ):

		# creates seven movie dictionaries - one per age group - that 
		# has MovieID as key and as variables:
		# 0) The sum of ratings;
		# 1) The number of users that rated that movie;
		# 2) The average calculated as: sum_of_ratings/num_users_rated.
		_1Movies = {}
		_18Movies = {}
		_25Movies = {}
		_35Movies = {}
		_45Movies = {}
		_50Movies = {}
		_56Movies = {}

		# loops over the rating dictionary.
		for key, val in ratingDict.items():
			# gets the current rating and converts it to an integer value.
			rating = int(ratingDict[(key[0], key[1])][0])

			# for each age group inside the usersDict
			if usersDict[key[0]][1] == '1':
				addMovieRate(_1Movies, key[1], rating)
			elif usersDict[key[0]][1] == '18':
				addMovieRate(_18Movies, key[1], rating)
			elif usersDict[key[0]][1] == '25':
				addMovieRate(_25Movies, key[1], rating)
			elif usersDict[key[0]][1] == '35':
				addMovieRate(_35Movies, key[1], rating)
			elif usersDict[key[0]][1] == '45':
				addMovieRate(_45Movies, key[1], rating)
			elif usersDict[key[0]][1] == '50':
				addMovieRate(_50Movies, key[1], rating)
			elif usersDict[key[0]][1] == '56':
				addMovieRate(_56Movies, key[1], rating)
		
		# calculates the dictionary maximum index available per gender group
		maxIndexes = calcMaxIndex([ _1Movies, _18Movies, _25Movies, _35Movies, _45Movies, _50Movies, _56Movies ])

		# returns the first n keys of the best rated movies for each age group.
		# When movies have the same rating, they are ordered by number of votes received
		_1MoviesKey = sorted(_1Movies.keys(), key=lambda x: (_1Movies[x][2], _1Movies[x][1]), reverse = True)[0:maxIndexes[0]]
		_18MoviesKey = sorted(_18Movies.keys(), key=lambda x: (_18Movies[x][2], _18Movies[x][1]), reverse = True)[0:maxIndexes[1]]
		_25MoviesKey = sorted(_25Movies.keys(), key=lambda x: (_25Movies[x][2], _25Movies[x][1]), reverse = True)[0:maxIndexes[2]]
		_35MoviesKey = sorted(_35Movies.keys(), key=lambda x: (_35Movies[x][2], _35Movies[x][1]), reverse = True)[0:maxIndexes[3]]
		_45MoviesKey = sorted(_45Movies.keys(), key=lambda x: (_45Movies[x][2], _45Movies[x][1]), reverse = True)[0:maxIndexes[4]]
		_50MoviesKey = sorted(_50Movies.keys(), key=lambda x: (_50Movies[x][2], _50Movies[x][1]), reverse = True)[0:maxIndexes[5]]
		_56MoviesKey = sorted(_56Movies.keys(), key=lambda x: (_56Movies[x][2], _56Movies[x][1]), reverse = True)[0:maxIndexes[6]]

		# prints out the ranking splitted by age group. The report is composed by:
		# 1) Ranking
		# 2) Movie - The movie title
		# 3) Avg Rating - The average rating
		# 4) Votes - The number of votes received by the movie
		printTable(_1Movies, _1MoviesKey, 'Under 18')
		printTable(_18Movies, _18MoviesKey, '18-24')
		printTable(_25Movies, _25MoviesKey, '25-34')
		printTable(_35Movies, _35MoviesKey, '35-44')
		printTable(_45Movies, _45MoviesKey, '45-49')
		printTable(_50Movies, _50MoviesKey, '50-55')
		printTable(_56Movies, _56MoviesKey, '56+')
		
# if the arguments given in input are not 3 the script will stop.
else:
	sys.exit('You haven\'t provided the correct number of arguments (2)')