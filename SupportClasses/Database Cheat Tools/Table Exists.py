import sqlite3

conn = sqlite3.connect('../Meeting Minutes.db')
c = conn.cursor()
try:
	with conn:
		c.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='meetings'")
		print(c.fetchall())
except Exception as e:
	pass
