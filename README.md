# <p align="center">CalendarIT Telegram Bot

<p align="center">A simple, but extensible Python Telegram bot, can post acquainted with what is happening today, tomorrow or what happened 20 years ago to 
channel.</p>

<h2><a href='https://calendarit.ru'>CalendarIT.ru</a> - official web site</h2>
<h2><a href='https://t.me/calendarit'>@CalendarIT</a> - link to Telegram channel</h2>
	
## Getting started

This bot get dates from SQLite database file, and post it to telegram channel.

* Installation using pip (a Python package manager):

```
$ git clone https://github.com/CodeByZen/calendarit-telegram-bot.git
$ cd calendarit-telegram-bot
$ pip install -r requirements.txt
$ python3 app.py
```

## Features

|feature|description|
|:---:|---|
|post dates|Get dates from database in several formats like: full date (13/01/2022), day of year (256), day of week like last friday of may, or monday on 3th week in august|
|several post methods|With image or without. in DB folder images subfolder exist, contain images with names as ID in database. If image file exist, bot post date as photo with caption.|
|commands| /puzzle - Bot generates scrabble like board where users can search exists words, /show - command show today dates, can use arguments in format /show Year Month DayOfMonth DayOfYear DayOfWeek WeekOfMonth to show concrete day date, /post -  for immediate post the dates to channel and some other commands can be found in /help |
|feedback function|All non-admins can send something to bot directly, and bot forward those messages to admin, admin can reply to this messages and users receive messages from admin|

With best regards to <a href="https://github.com/eternnoir/pyTelegramBotAPI">PyTelegramBot</a> developers, thanks for your hard work.
