analyze_movies
==============

This repo contains the Python script to analyze the MovieLens 1M dataset and provide a simple CLI reporting system for it. The script can be executed via command line using this syntax: ./analyze_movies.py (gender|agegroup) &lt;number&gt;
* The first argument is the grouping. For example, if gender is selected, then two lists will be output: top movies as rated by men, and top movies as rated by women. If agegroup is selected, 7 lists should be output, as specified in the dataset README.
* The &lt;number&gt; is how many to output. If there are fewer than &lt;number&gt; movies, output them all.
An example invocation would, therefore be "./analyze_movies.py age 20"
