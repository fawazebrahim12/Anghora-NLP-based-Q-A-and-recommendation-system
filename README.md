# Anghora README #

This is an NLP Based question answering system with a recommendation system integrated in it.

It has three parts
1. A question answering system which with the help of a set of API's answers questions.
2. A Categorization system which uses Naive Bayes Classifier to classify questions the NBC is trained upon a dataset of 2300 questions of 10 categories.
3. A Recommendation System which is based on Pearson Collaberation, used to recommend users a set of questions they might be interested in based on their previous queries.

How to set up? 

### Backend ###

* Download Sr.Anghora
* pip install wolframalpha , apiai , googlemaps and flask #I'm assuming other small dependencies are already installed like requests etc.
* Run server.py (Sr.Anghora/server.py)

You will see something like :
/* Running server at 127.0.0.1:5000 */

The server returns a json format which has answers to the query.
the server accepts two parameters a query and user id(return -1 if you do not need recommendation)

Ping server like localhost:5000/?q=somequery&id=1

output will be a json object.

### UI (Parsing the json object)###

******Creating Database for users*******

*Create a database for the users with fields like id,name,emailid and password.

OR

*Import users.sql  (UI/users.sql) to your database # a table wit 10 users will be created
* Enter login credentials of the database in UI/login.php and UI/registration.php
*Run apache server or any equivalent server for php
*Run frontend.php (UI/frontend.php) in the browser

That's it Enter any query and see the answers........

### Categorization (ML) ###

* pip install textblob
* python -m textblob.download_corpora
* Run categorize.py (categorize(ML)/categorize.py) on result15.csv(dataset containing 2300 queries)

------it will take an hour or so depending on your RAM, so I recommend you to extract the output of the program i.e----------

* Extract my_classifier.pickle file.

and check the result

* Run query.py

This module is to categorize the question to one of the 10 categories. But in the server program I've used alchemy API which s faster in execution and accuracy is also high and it categorizes to one of the 23 categorize. 

### Recommendation System ###

It is already integrated with he server so no need to run, I've put 10 users profile(their questions asked and their category), you can replace these file with your users.