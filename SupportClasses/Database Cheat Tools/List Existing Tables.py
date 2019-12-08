import sqlite3

conn = sqlite3.connect('Meeting Minutes.db')
c = conn.cursor()
try:
	with conn:
		c.execute('''SELECT 
					    name
					FROM 
					    sqlite_master 
					WHERE 
					    type ='table' AND 
					    name NOT LIKE 'sqlite_%';''')
		print(c.fetchall())
		input()
except Exception as e:
	pass