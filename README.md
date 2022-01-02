# Make Highlight 

**Members**：

夏  - 736001469@qq.com

邱 - 1712590429@qq.com

方 - 874524395@qq.com



[@toc]



## What is it？



This is a **software architecture** course project.

It was originally designed to allow you to learn new words while reading articles, and it can **record the words** you extract and display them in other articles.

We added the ability to **highlight** new words for this project.

[Original project Reference](http://121.4.94.30:3000/mrlan/EnglishPal)



## Run it on a local machine

`python3 main.py`

Make sure you have the SQLite database file in `app/static` (see below).



## Importing articles

All articles are stored in the `article` table in a SQLite file called
`app/static/wordfreqapp.db`



### Adding new articles

To add articles, open and edit `app/static/wordfreqapp.db` using DB Browser for SQLite (https://sqlitebrowser.org).



### Exporting the database

Export wordfreqapp.db to wordfreqapp.sql using the following commands:

- sqlite3 wordfreqapp.db

- .output wordfreqapp.sql

- .dump

- .exit

Put wordfreqapp.sql (not wordfreqapp.db) under version control.

### Creating SQLite file from wordfreqapp.sql


Create wordfreqapp.db using this command: `cat wordfreqapp.sql |
sqlite3 wordfreqapp.db`.  Delete wordfreqapp.db first if it exists.


### Uploading wordfreqapp.db to the server

`pscp wordfreqapp.db lanhui@118.*.*.118:/home/lanhui/englishpal/app/static`



## What did we do based on the original project

### Task1

We added the new word **highlighting** function to the original project



### Task2

Using the **blueprints** in Flask to **refactored** some of the code



### Task3

**Commented** out some of the new code 



### Task4

**Added and improved** some functions, make the use more user-friendly



## Feedback

We welcome feedback on EnglishPal.
