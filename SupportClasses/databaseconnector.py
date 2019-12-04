import sqlite3

class DatabaseConnector:
	def __init__(self):
		self.conn = sqlite3.connect('Meeting Minutes.db')
		self.c = self.conn.cursor()





