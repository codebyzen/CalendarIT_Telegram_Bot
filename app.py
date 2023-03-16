import re
import random
import sys
import threading
import time
from gears.app_db import app_db
from gears.app_functions import app_functions
import telebot # pyTelegramBotAPI=4.9.0
from telebot import types, util
import schedule # schedule=1.1.0
import os, datetime
from gears.avatar_update.avatar_update import avatar_update
from gears.puzzle.word_grid import WordGrid
from gears.puzzle.puzzle_image import puzzle_image

API_TOKEN = 'bot token'
CHAT_ID = 123 # test chat

ADMIN_ID = 321 # admin telegram ID

bot = telebot.TeleBot(API_TOKEN)

""" DEBUG """
debug = True
debug_messages = ""

bot.set_my_commands([
	telebot.types.BotCommand("/start", "Start bot"),
	telebot.types.BotCommand("/help", "Show help")
])

def d(any):
	if (debug==True): 
		print(any)


def getDates(show_fields=None):
	global debug_messages # think we inside the class here

	db = app_db()
	db.db_connection_create()

	core_functions = app_functions(db.cursor, db.sqlite_connection)
	dates = core_functions.getTheDate(show_fields)
	debug_messages = core_functions.query_debug

	db.db_connection_close()

	datesItems = []

	for i in dates:
		datesText = "*"+i['title']+"* _("+str(i['year'])+")_"+"\n"
		datesText += i['already']+" "+str(i['old'][0])+" "+i['old'][1]+" _("+str(i['day'])+" "+str(i['month'])+" "+str(i['year'])+")_"+"\n\n"
		datesText += i['description']+"\n"
		datesText += "\n\n\n"
		datesItems.append({"picture": i['picture'], "text": datesText})

	# pprint(datesItems)
	return datesItems

def postDates(chat_id, dateFields=None) -> None:
	"""Send the beep message."""

	# update avatar in channel
	if (chat_id==CHAT_ID):
		channel_avatar_update()

	dates = getDates(dateFields)

	for i in dates:
		if (i["picture"]==None):
			bot.send_message(chat_id, text=i["text"], parse_mode = "markdown")
		else:
			bot.send_photo(chat_id, photo=open(i["picture"], 'rb'), caption=i["text"], parse_mode = "markdown")

	if len(dates)==0:
		bot.send_message(chat_id, text="Сегодня нет дат из календаря 😕\nНо если у Вас есть предложения пишите нам https://t.me/calendarit_bot", parse_mode = "markdown")


@bot.message_handler(commands=['start'])
def postDatesByCommand(message):
	if (message.from_user.id != ADMIN_ID):
		bot.send_message(message.chat.id, text="Подписывайтесь ➡️ [@CalendarIT](https://t.me/calendarit)\n\nИли отправьте мне сообщение, я передам его комманде!", parse_mode = "markdown")
	else:
		bot.send_message(message.chat.id, text="I'm here", parse_mode = "markdown")


@bot.message_handler(commands=['post'])
def postDatesByCommand(message):
	if (message.from_user.id != ADMIN_ID):
		return
	else:
		postDates(CHAT_ID)

# /show Y	M  d  DoY DoW WoM
message_regexp_string = r"/show((\s[\d]*)?(\s[\d]*)?(\s[\d]*)?(\s[\d]*)?(\s[\d]*)?(\s[\d]*)?)?"
@bot.message_handler(regexp=message_regexp_string)
def showDates(message):
	if (message.from_user.id != ADMIN_ID):
		return
	else:
		show_fields = {
			'year': 0,
			'month_of_year': 0,
			'day_of_month': 0,
			'day_of_year': 0,
			'day_of_week': 0,
			'week_of_month': 0
		}
		m = re.search(message_regexp_string, message.text)
		if m:
			matches_count = len(m.groups())+1
			show_fields_counter = 0
			is_extended_query = False
			for i in range(2,matches_count):
				if m.group(i):
					is_extended_query = True
					show_fields[list(show_fields)[show_fields_counter]] = int(m.group(i).strip())
					show_fields_counter+=1

			if is_extended_query:
				bot.send_message(message.chat.id, "Extended date", parse_mode="markdown")
				# print(show_fields)
				postDates(message.chat.id, show_fields)
			else:
				bot.send_message(message.chat.id, "Simple date", parse_mode="markdown")		
				postDates(message.chat.id)
			# d(show_fields)


def checkDates():
	global debug_messages # think we inside the class here

	db = app_db()
	db.db_connection_create()

	core_functions = app_functions(db.cursor, db.sqlite_connection)
	result = core_functions.checkDates()
	debug_messages = core_functions.query_debug

	db.db_connection_close()

	return result


@bot.message_handler(commands=['help'])
def showDates(message):
	if (message.from_user.id != ADMIN_ID):
		bot.send_message(message.chat.id, text="Join to ➡️ [@CalendarIT](https://t.me/calendarit)", parse_mode = "markdown")
	else:
		preparedMessageText = [
			"/post - post dates to channel",
			"/show - show dates here (optional: /show Y M d DoY DoW WoM)",
			"/check - check dates",
			"/token - get admin token",
			"/datenow - to check time",
			"/puzzle - generate puzzle",
			"/updateavatar - update avatar",
			"/deleteavatar - delete avatar",
		]
		bot.send_message(message.chat.id, "\n".join(preparedMessageText), parse_mode="markdown")

@bot.message_handler(commands=['token'])
def showDates(message):
	if (message.from_user.id == ADMIN_ID):
		db = app_db()
		db.db_connection_create()
		core_functions = app_functions(db.cursor, db.sqlite_connection)
		preparedMessageText = core_functions.get_admin_token(ADMIN_ID)
		db.db_connection_close()
		bot.send_message(message.chat.id, preparedMessageText, parse_mode="markdown")


@bot.message_handler(commands=['datenow'])
def showDates(message):
	if (message.from_user.id == ADMIN_ID):
		dt = datetime.datetime.now()
		weekday = dt.weekday()+1

		posthour = "08"
		if (weekday==6 or weekday==7):
			posthour = "10"

		msg = "*date:* "+dt.strftime("%d/%m/%Y, %H:%M:%S")+"\n*weekday:* "+str(weekday)+"\n*today we post at:* "+posthour
		bot.send_message(message.chat.id, msg, parse_mode="markdown")

@bot.message_handler(commands=['check'])
def showDates(message):
	if (message.from_user.id == ADMIN_ID):
		bot.send_message(message.chat.id, "Checking...", parse_mode="markdown")
		msg = checkDates()
		bot.send_message(message.chat.id, msg, parse_mode="markdown")

def getPostTime(dt):
	randmin = random.randint(0, 15)

	posthour = "08"

	weekday = dt.weekday()+1

	if (weekday==6 or weekday==7):
		posthour = "10"

	if randmin<10: 
		randmin = "0"+str(randmin)
	else:
		randmin = str(randmin)

	return posthour+":"+randmin

@bot.message_handler(commands=['deleteavatar'])
def channel_avatar_update_command(message):
	if (message.from_user.id == ADMIN_ID):
		
		db = app_db()
		db.db_connection_create()
		core_functions = app_functions(db.cursor, db.sqlite_connection)
		msg_id = core_functions.get_setting_by_name('avatar_update_message_id')
		db.db_connection_close()
		
		if msg_id!=None:
			bot.delete_message(chat_id=CHAT_ID, message_id=msg_id)
		
		bot.delete_chat_photo(chat_id=CHAT_ID)

@bot.message_handler(commands=['updateavatar'])
def channel_avatar_update_command(message):
	if (message.from_user.id == ADMIN_ID):
		channel_avatar_update()

def channel_avatar_update():
	au = avatar_update()
	au.generate()
	
	db = app_db()
	db.db_connection_create()
	core_functions = app_functions(db.cursor, db.sqlite_connection)
	msg_id = core_functions.get_setting_by_name('avatar_update_message_id')
	db.db_connection_close()
	if msg_id!=None:
		bot.delete_chat_photo(chat_id=CHAT_ID)
		bot.delete_message(chat_id=CHAT_ID, message_id=msg_id)
	bot.set_chat_photo(chat_id=CHAT_ID, photo=open("assets/avatar_update/channel_avatar_date.jpg", 'rb'))
	# execute channel_post_handler function and intercept message_id from new_chat_photo
	# save it to database
	

@bot.message_handler(commands=['puzzle'])
def puzzle_generate(message):
	if (message.from_user.id == ADMIN_ID):
		grid = WordGrid(size=20, words_file='assets/puzzle/words-ru.txt', cheated=True)
		au = puzzle_image()
		au.generate(grid.puzzle)
		
		bot.send_message(chat_id=message.chat.id,  text=", ".join(grid.words), parse_mode="markdown")
		img1 = open("assets/puzzle/puzzle_1.jpg", 'rb')
		img2 = open("assets/puzzle/puzzle_2.jpg", 'rb')
		bot.send_photo(chat_id=message.chat.id, photo=img1, has_spoiler=False, caption="Еще одна наша еженедельная рубрика!\n\n🧐 В этом ребусе загаданы 15 IT терминов! Разгадывайте, делитесь в комментариях!\n\nВ конце недели откроем все слова!\n\n#puzzle")
		bot.send_photo(chat_id=message.chat.id, photo=img2, has_spoiler=True)
		img1.close()
		img2.close()

# intercept new_chat_photo and store 
@bot.channel_post_handler(content_types=['new_chat_photo'])
def handle_messages_new_chat_photo(message):
	if message.chat.id == CHAT_ID:
		db = app_db()
		db.db_connection_create()
		core_functions = app_functions(db.cursor, db.sqlite_connection)
		core_functions.set_setting('avatar_update_message_id',message.message_id)
		db.db_connection_close()

# delete system message delete_chat_photo from channel
@bot.channel_post_handler(content_types=['delete_chat_photo'])
def handle_messages_delete_chat_photo(message):
	if message.chat.id == CHAT_ID:
		bot.delete_message(chat_id=CHAT_ID, message_id=message.message_id)


# send messages from bot to admin
@bot.message_handler(content_types=['animation', 'audio', 'contact', 'document', 'location', 'photo', 'sticker', 'text', 'venue', 'video', 'video_note', 'voice'])
def chatting(message: types.Message):
	if (message.from_user.id!=ADMIN_ID):
		# reply to user
		bot.reply_to(message=message,text="Услышали Вас. Скоро ответим.")
		# forward to admin
		message_on_admin_chat = bot.forward_message(chat_id=ADMIN_ID,from_chat_id=message.from_user.id, message_id=message.id)

		db = app_db()
		db.db_connection_create()
		core_functions = app_functions(db.cursor, db.sqlite_connection)
		core_functions.feedback_store(
			from_user_id=message.from_user.id,
			from_user_name=message.from_user.username,
			message_id=message_on_admin_chat.id
		)
		db.db_connection_close()

	if (message.from_user.id==ADMIN_ID):
		
		db = app_db()
		db.db_connection_create()
		core_functions = app_functions(db.cursor, db.sqlite_connection)
		to_user = core_functions.feedback_get_by_message_id(message.reply_to_message.id)
		db.db_connection_close()

		bot.copy_message(chat_id=to_user, from_chat_id=message.chat.id, message_id=message.id)






# ============================= MAIN THREAD =============================





if __name__ == '__main__':

	os.environ['TZ'] = 'Europe/Moscow'
	time.tzset()

	daynow = datetime.datetime.now().day

	# get today post time (hour int)
	posttime = getPostTime(datetime.datetime.now())
	
	# schedule postDates
	schedule.every().day.at(posttime).do(postDates, CHAT_ID).tag(CHAT_ID)

	# get updates from Telegram
	threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()

	while True:
		# check the day changed, get new time for posting
		if (daynow!=datetime.datetime.now().day):
			daynow = datetime.datetime.now().day
			schedule.clear()
			posttime = getPostTime(datetime.datetime.now())
			schedule.every().day.at(posttime).do(postDates, CHAT_ID).tag(CHAT_ID)

		schedule.run_pending()
		time.sleep(1)