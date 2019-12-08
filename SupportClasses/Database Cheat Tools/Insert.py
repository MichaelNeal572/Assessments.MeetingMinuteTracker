import sqlite3

conn = sqlite3.connect('Meeting Minutes.db')
c = conn.cursor()
try:
	with conn:
		items = [("F","1"),
				("F","2"),
				("PTL","1")]
		sql = "INSERT INTO meetings (meetingPrefix, meetingNumber) VALUES (?, ?)"
		c.executemany(sql,items)
		conn.commit()

		items = [(1,"test1"),
				(2,"test2"),
				(3,"test3")]
		sql = "INSERT INTO items (itemID, itemName) VALUES (?, ?)"
		c.executemany(sql,items)
		conn.commit()

		items = [(1,1,"F","TBD", "TBD"),
				(2,2,"F", "TBD","TBD"),
				(3,1,"PTL", "TBD", "TBD")]
		sql = '''INSERT INTO meeting_item_status
		(itemID, meetingNumber, meetingPrefix, statusActionsRequired,statusPersonResponsible) 
		VALUES 
		(?, ?, ?, ?, ?)'''
		c.executemany(sql,items)
		conn.commit()

except Exception as e:
	print(f"Error: {str(e)}")
else:
	print("Success")

