import itertools
from math import ceil
import datetime
import calendar as cal
import os
from gears.app_pronounce import app_pronounce
import hashlib
import random
import string


class app_functions:

	cur = None
	con = None
	query_debug = ''

	def __init__(self, cur, con):
		self.cur = cur
		self.con = con

	def feedback_store(self, from_user_id, from_user_name, message_id):
		q = "SELECT * FROM feedback WHERE from_user_id = ?"
		self.cur.execute(q, [str(from_user_id)])
		total = self.cur.fetchall()
		if (total==None or len(total)==0):
			q = "INSERT INTO feedback VALUES(NULL, ?, ?, ?);"
			# itdates_functions_logger.debug(q)
			self.cur.execute(q, [from_user_id, from_user_name, message_id])
			self.con.commit()
		else:
			q = "UPDATE feedback SET message_id=? WHERE from_user_id = ?"
			# itdates_functions_logger.debug(q)
			self.cur.execute(q, [message_id, from_user_id])
			self.con.commit()
		return True

	def feedback_get_by_message_id(self, message_id):
		q = "SELECT * FROM feedback WHERE message_id = ?"
		self.cur.execute(q, [str(message_id)])
		total = self.cur.fetchall()
		if (total!=None and len(total)>0):
			return total[0]['from_user_id']
		return None

	def get_admin_token(self, admin_id):
		# itdates_functions_logger.debug("get_admin_token")
		salt = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
		new_token = hashlib.md5(str(str(datetime.datetime.now())+str(admin_id)+str(salt)).encode('utf-8')).hexdigest()
		expire = datetime.datetime.now() + datetime.timedelta(days=1)

		self.cur.execute("SELECT * FROM tokens WHERE user_id = "+str(admin_id))
		total = self.cur.fetchall()
		if (total==None or len(total)==0):
			# itdates_functions_logger.debug("No admin in token")
			q = "INSERT INTO tokens VALUES(NULL, '"+str(admin_id)+"', '"+str(new_token)+"', '"+str(expire)+"');"
			# itdates_functions_logger.debug(q)
			self.cur.execute(q)
			self.con.commit()
			# itdates_functions_logger.debug(new_token)
			return new_token
		else:
			# itdates_functions_logger.debug("tokens exists")
			# itdates_functions_logger.debug(str(len(total)))
			for v in total:
				v_date = datetime.datetime.strptime("2023-01-18 21:21:19.549276", "%Y-%m-%d %H:%M:%S.%f")
				if v_date < datetime.datetime.now():
					# itdates_functions_logger.debug("token expired")
					q = "UPDATE tokens SET token = '"+str(new_token)+"', expired='"+str(expire)+"' WHERE user_id = '"+str(admin_id)+"'"
					# itdates_functions_logger.debug(q)
					self.cur.execute(q)
					self.con.commit()
					return new_token
				else:
					# itdates_functions_logger.debug("token from database")
					return v['token']

	def get_setting_by_name(self,setting_name):
		self.cur.execute("SELECT * FROM settings WHERE name = ?", [str(setting_name)])
		total = self.cur.fetchall()
		if (total!=None and len(total)>0):
			return total[0]['value']
		else: 
			return None

	def set_setting(self,name,value):
		is_exist = self.get_setting_by_name(name)
		if is_exist==None:
			q = "INSERT INTO settings VALUES(NULL, ?, ?);"
			self.cur.execute(q, [str(name), str(value)])
			self.con.commit()
		else:
			q = "UPDATE settings SET value = ? WHERE name = ?"
			self.cur.execute(q, [str(value), str(name)])
			self.con.commit()

	def get_week_of_month(self,dt):
		""" Returns the week of the month for the specified date.
		"""

		first_day = dt.replace(day=1)

		dom = dt.day
		adjusted_dom = dom + first_day.weekday()

		return int(ceil(adjusted_dom/7.0))

	def get_day_of_week(self,dt):
		""" Returns the day of week for the specified date.
		"""
		day_of_week = int(dt.isoweekday())
		return day_of_week

	def get_last_weekday(self,year,month,weekday,weekcount=0):
		""" Returns the last day (1-7) of month for the specified date.
		"""
		if (weekcount==0):
			last_friday = max(week[weekday-1] for week in cal.monthcalendar(year, month))
		else:
			last_friday_gen = (week[weekday-1] for week in cal.monthcalendar(year, month))
			last_friday = next(itertools.islice(last_friday_gen, weekcount, None))
		return last_friday

	def get_month_week_num(self,year,month,day,weekday):
		counter = 1
		for week in cal.monthcalendar(year, month):
			if (week[weekday-1]!=0):
				if (int(day)==int(week[weekday-1])):
					return counter
				counter += 1
		return 0

	def getTotalCountDates(self):

		self.cur.execute("SELECT COUNT(id) as cnt FROM `dates`")
		record = self.cur.fetchall()
		if (record):
			return record[0].cnt

	def compileExtendedSQLQuery(self, fields):

		if (fields["day_of_year"]!=0):
			q = "SELECT * FROM dates WHERE day_of_year = "+fields["day_of_year"]+";"
		
		if (fields["day_of_week"]!=0 and fields["week_of_month"]==0):
			q = "SELECT * FROM dates WHERE month_of_year = "+str(fields["month_of_year"])+" AND day_of_week = "+str(fields["day_of_week"])+" AND week_of_month IS NULL;"

		if (fields["day_of_week"]!=0 and fields["week_of_month"]!=0):
			q = "SELECT * FROM dates WHERE month_of_year = "+str(fields["month_of_year"])+" AND day_of_week = "+str(fields["day_of_week"])+" AND week_of_month = "+str(fields["week_of_month"])+";"

		if (fields["day_of_month"]!=0 and fields['month_of_year']!=0):
			q = "SELECT * FROM dates WHERE month_of_year = "+str(fields["month_of_year"])+" AND day_of_month = "+str(fields["day_of_month"])+";"

		if (fields["year"]!=0 and fields["month_of_year"]!=0 and fields["day_of_month"]!=0):
			date = datetime.datetime.strptime(str(fields["year"])+"-"+str(fields["month_of_year"])+"-"+str(fields["day_of_month"]), "%Y-%m-%d").date()
			day_of_year = date.timetuple().tm_yday
			
			q = "SELECT *, "+str(date.month)+" AS month_of_year, "+str(date.day)+" AS day_of_month FROM dates WHERE day_of_year = "+str(day_of_year)

			week_of_month = self.get_week_of_month(date)
			day_of_week = self.get_day_of_week(date)
			q += " OR (month_of_year = "+str(fields["month_of_year"])+" AND week_of_month = "+str(week_of_month)+" AND day_of_week = "+str(day_of_week)+")"
			q += " OR (month_of_year = "+str(fields["month_of_year"])+" AND week_of_month IS NULL AND day_of_week = "+str(day_of_week)+")"
			q += " OR (month_of_year = "+str(fields["month_of_year"])+" AND day_of_month = "+str(fields["day_of_month"])+")"

		return q

	def compileSimpleSQLQuery(self, concreteDate=None):
		
		if (concreteDate==None):
			datenow = datetime.datetime.now()
		else:
			datenow = concreteDate

		# datenow = datetime.datetime.strptime("2022-9-13", "%Y-%m-%d").date()
		# datenow = datetime.datetime.strptime("2022-1-30", "%Y-%m-%d").date()
		# datenow = datetime.datetime.strptime("2023-10-20", "%Y-%m-%d").date()
		
		day = datenow.strftime("%d").lstrip("0")
		month = datenow.strftime("%m").lstrip("0")
		year = datenow.strftime("%Y").lstrip("0")

		day_of_year = datenow.timetuple().tm_yday
		# week_of_month = self.get_week_of_month(datenow)
		day_of_week = self.get_day_of_week(datenow)
		month_week_num = self.get_month_week_num(int(year),int(month),int(day),int(day_of_week))
		

		q = """
			SELECT *, """+str(month)+""" AS month_of_year, """+str(day)+""" AS day_of_month
			FROM dates
			WHERE
				(month_of_year = """+str(month)+""" AND day_of_month = """+str(day)+""")
				OR
				(day_of_year = """+str(day_of_year)+""")
				OR
				(month_of_year = """+str(month)+""" AND day_of_week = """+str(day_of_week)+""" AND week_of_month = """+str(month_week_num)+""")
		"""

		# if current day is last week_day
		last_week_day = self.get_last_weekday(int(year),int(month),day_of_week,0)
		if (last_week_day==day):
			q += """ OR (month_of_year = """+str(month)+""" AND day_of_week = """+str(day_of_week)+""" AND day_of_month IS NULL AND week_of_month IS NULL)"""
		return q

	def checkDates(self):

		def daterange(start_date, end_date):
			for n in range(int((end_date - start_date).days)):
				yield start_date + datetime.timedelta(n)

		dateData = []
		start_date = datetime.date(2013, 1, 1)
		end_date = datetime.date(2015, 6, 2)
		for single_date in daterange(start_date, end_date):
			q = self.compileSimpleSQLQuery(single_date)
			dateData.extend(self.getTheDateFromDB(q))
		
		q = "SELECT * FROM dates"
		self.cur.execute(q)
		total = self.cur.fetchall()
		
		for dbitem in total:
			for datesitem in dateData:

				if (dbitem["id"]==datesitem["id"]):
					dbitem["isok"] = True
		

		msg = "Result:"
		msg_ok_count = 0
		for i in total:
			if "isok" not in i:
				msg+="\nID: "+str(i["id"])+" has error!"
			else:
				msg_ok_count += 1

		return msg+"\nDates checked: "+str(msg_ok_count)

	# берем дату за сегодня
	def getTheDate(self, fields = None):

		if (fields!=None):
			q = self.compileExtendedSQLQuery(fields)
		else:
			q = self.compileSimpleSQLQuery()
			
		dateData = self.getTheDateFromDB(q)

		return dateData


	def getTheDateFromDB(self, q):
		self.query_debug = q

		out = []

		self.cur.execute(q)
		total = self.cur.fetchall()
		if (total==None):
			return out


		lang = app_pronounce.config['ln']

		for v in total:

			datenow = datetime.datetime.now()
			dayNow = datenow.strftime("%d").lstrip("0")
			yearNow = datenow.strftime("%Y").lstrip("0")

			itemObject = {
				'id': v['id'],
				'originalyear': v['year'],
				'year': v['year'] if v['year']>0 else yearNow,
				'day': v['day_of_month'] if v['day_of_month'] != 0 else dayNow,
				'month': app_pronounce.ln[lang]['months'][v['month_of_year']-1],
				'title': v['title'],
				'already': app_pronounce.getAlready(v['day_of_month'],v['month_of_year']),
				'old': app_pronounce.getYearsPronounce(app_pronounce,int(yearNow)-v['year']) if v['year']>0 else 'party',
				'current': True if v['day_of_month']==dayNow else False,
				'description': v['text'],
				'picture': self.getImage(str(v['id'])+'.jpg')
			}

			out.append(itemObject)

		return out


	def getImage(self, filename):

		path = "./db/images/" # production

		out = None

		if (filename!=None and filename!=False and filename!=''):
			if (os.path.isfile(path+filename)):
				out = path+filename

		return out





# unuserd
	# def sanitize_title_with_translit(text):

	# 	symbols = (
	# 		u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
	# 		(*list(u'abvgdee'), 'zh', *list(u'zijklmnoprstuf'), 'kh', 'z', 'ch', 'sh', 'sh', '',
	# 		'y', '', 'e', 'yu','ya', *list(u'ABVGDEE'), 'ZH',
	# 		*list(u'ZIJKLMNOPRSTUF'), 'KH', 'Z', 'CH', 'SH', 'SH', *list(u'_Y_E'), 'YU', 'YA', ' ')
	# 	)

	# 	coding_dict = {source: dest for source, dest in zip(*symbols)}
	# 	translate = lambda x: ''.join([coding_dict[i] for i in x])

	# 	text = text.lower()


	# 	return translate(text)




