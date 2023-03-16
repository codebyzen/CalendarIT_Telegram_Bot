import datetime
import sqlite3

class app_db:

	# db connection
	cursor = None
	sqlite_connection = None

	def db_connection_create(self):
		# use this for convert object returned from sqlite to dict
		def dict_factory(cursor, row):
			d = {}
			for idx, col in enumerate(cursor.description):
				d[col[0]] = row[idx]
			return d

		try:
			self.sqlite_connection = sqlite3.connect('./db/sqlite_python.db') # production

			self.sqlite_connection.row_factory = dict_factory
			self.cursor = self.sqlite_connection.cursor()

			sqlite_select_query = "select sqlite_version();"
			self.cursor.execute(sqlite_select_query)
			record = self.cursor.fetchall()

		except sqlite3.Error as error:
			file = open('log.txt', 'a')
			file.write(str(datetime.datetime.now()) + " SQLite Erroro: "+error)
			file.close()
			quit()


	def db_connection_close(self):
		self.cursor.close()
		self.sqlite_connection.close()