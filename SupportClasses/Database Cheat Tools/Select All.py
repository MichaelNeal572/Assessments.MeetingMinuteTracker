import sqlite3

conn = sqlite3.connect('Meeting Minutes.db')
c = conn.cursor()
try:
	with conn:
		print("## meetings ##")
		for row in c.execute("SELECT * FROM meetings"):
			print(row)
		print("## meeting_types ##")
		for row in c.execute("SELECT * FROM meeting_types"):
			print(row)
		print("## items ##")
		for row in c.execute("SELECT * FROM items"):
			print(row)
		print("## meeting_item_status ##")
		for row in c.execute("SELECT * FROM meeting_item_status"):
			print(row)
		print("## Exists MANCO MEETING##")
		c.execute('''SELECT EXISTS(SELECT * FROM meetings
				WHERE meetingPrefix = :prefix) AS found
			''',
			{"prefix": "M"})
		print(c.fetchone())
		print("## lastest Finance MEETING##")
		c.execute('''SELECT MAX(meetingNumber) FROM meetings
				WHERE meetingPrefix = :prefix 
			''',
			{"prefix": "F"})
		print(c.fetchone()[0])
		print("## get prefix by type##")
		c.execute('''SELECT meetingPrefix FROM meeting_types
				WHERE meetingType = :type
			''',
			{"type":"Project Team Leaders"})
		print(c.fetchone()[0])
		print("## get meeting items by meeting##")
		c.execute('''SELECT itemName FROM items
				JOIN meeting_item_status ON items.itemID = meeting_item_status.itemID
				WHERE  meeting_item_status.meetingPrefix= :prefix 
				AND meeting_item_status.meetingNumber= :num
			''',
			{"prefix":"F",
			"num":2})
		print([_[0] for _ in c.fetchall()])
except Exception as e:
	print(e)