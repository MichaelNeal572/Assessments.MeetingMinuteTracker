import sqlite3

conn = sqlite3.connect('../Meeting Minutes.db')
c = conn.cursor()

try:
	with conn:
		c.execute("DROP TABLE meeting-item-status")
		c.execute("DROP TABLE item_status")
		c.execute("DROP TABLE items")
		c.execute("DROP TABLE meeting_types")
		c.execute("DROP TABLE meetings")

except Exception as e:
	pass