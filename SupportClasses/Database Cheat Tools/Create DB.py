import sqlite3

conn = sqlite3.connect('Meeting Minutes.db')
c = conn.cursor()
try:
	with conn:
		##Create meetings Table##
		c.execute('''
			CREATE TABLE meetings(
				meetingNumber integer NOT NULL,
				meetingPrefix text NOT NULL REFERENCES meeting_types(meetingPrefix),
				PRIMARY KEY(meetingNumber, meetingPrefix)
			)
			''')
		#########################

		##Create meeting_types Table##
		c.execute('''
			CREATE TABLE meeting_types(
				meetingPrefix text NOT NULL UNIQUE,
				meetingType text NOT NULL UNIQUE,
				PRIMARY KEY (meetingPrefix)
			)
			''')
		currentMeetingTypes = [("M","MANCO"),
							("F","FINANCE"),
							("PTL","Project Team Leaders")]
		sql = "INSERT INTO meeting_types (meetingPrefix, meetingType) VALUES (?, ?)"
		c.executemany(sql,currentMeetingTypes)
		conn.commit()
		#########################
		
		##Create meeting_types Table##
		c.execute('''
			CREATE TABLE items(
				itemID integer NOT NULL PRIMARY KEY,
				itemName text NOT NULL
			)
			''')

		##Create meeting_types Table##
		c.execute('''
			CREATE TABLE meeting_item_status(
				itemID integer NOT NULL,
				meetingNumber integer NOT NULL,
				meetingPrefix text NOT NULL,
				statusActionsRequired text NOT NULL,
				statusPersonResponsible text NOT NULL,
				FOREIGN KEY(itemID) REFERENCES items(itemID),
				FOREIGN KEY(meetingNumber, meetingPrefix) REFERENCES meetings(meetingNumber, meetingPrefix) 
			)
			''')
except Exception as e:
	print(f"ERROR: {e}")
else:
	print("SUCCESS")