import sqlite3


class DataBase:

	def __init__(self):
		self.create_connect()

		try:
			self.cursor.execute(''' CREATE TABLE short_links (
													code TEXT PRIMARY KEY,
													link TEXT
												   ) 
							''')

		except sqlite3.OperationalError:
			pass

		self.break_connection()

	def create_connect(self):
		self.conn = sqlite3.connect('db.sqlite3', check_same_thread = False)
		self.cursor = self.conn.cursor()

	def break_connection(self):
		self.cursor.close()
		self.conn.close()

	def write(self, code, link):
		self.create_connect()

		self.cursor.execute(f''' INSERT INTO short_links (code, link) 
									VALUES ("{code}", "{link}") ''')
		self.conn.commit()

		self.break_connection()

	def return_unit(self, code):
		self.create_connect()

		sql = ' SELECT * FROM short_links WHERE code=?'

		self.cursor.execute(sql, [(code)])
		unit = self.cursor.fetchall()

		self.break_connection()

		return unit
