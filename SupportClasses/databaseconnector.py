import sqlite3

class DatabaseConnector:
	def __init__(self):
		self.conn = sqlite3.connect('Meeting Minutes.db')
		self.c = self.conn.cursor()
		self.initialize_database()

	##Database Initialization##
	def reinitialize_database(self):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				self.c.execute("DROP TABLE IF EXISTS meetings;")
				self.c.execute("DROP TABLE IF EXISTS items;")
				self.c.execute("DROP TABLE IF EXISTS meeting_item_status;")
				self.c.execute("DROP TABLE IF EXISTS meeting_types;")
		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		else:
			response = self.initialize_database()
		finally:
			return response
			

	def initialize_database(self):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				
				self.c.execute('''
					CREATE TABLE IF NOT EXISTS meetings(
						meetingNumber integer NOT NULL,
						meetingPrefix text NOT NULL REFERENCES meeting_types(meetingPrefix),
						PRIMARY KEY(meetingNumber, meetingPrefix)
					)
					''')

				self.c.execute('''
					CREATE TABLE IF NOT EXISTS meeting_types(
						meetingPrefix text NOT NULL UNIQUE,
						meetingType text NOT NULL UNIQUE,
						PRIMARY KEY (meetingPrefix)
					)
					''')

				self.c.execute('''
					CREATE TABLE IF NOT EXISTS items(
						itemID integer NOT NULL PRIMARY KEY,
						itemName text NOT NULL
					)
					''')

				self.c.execute('''
					CREATE TABLE IF NOT EXISTS meeting_item_status(
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
			response["status"]="Error"
			response["result"]=e
		else:

			return self.insert_initial_records()
	###########################

	##Read Statements##
	def get_meeting_types(self):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				self.c.execute("SELECT DISTINCT meetingType FROM meeting_types")
				response["result"]= [_[0] for _ in self.c.fetchall()]
		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response

	def get_meeting_prefix_by_type(self, meetingType):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				self.c.execute('''SELECT meetingPrefix FROM meeting_types
				WHERE meetingType = :type
					''',
					{"type":meetingType})
				response["result"]= self.c.fetchone()[0]

		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response

	def get_last_meeting_by_type(self, meetingPrefix):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				self.c.execute('''SELECT EXISTS(SELECT * FROM meetings
				WHERE meetingPrefix = :prefix) AS found
				''',
				{"prefix": meetingPrefix})
				if self.c.fetchone()[0]==0:
					response["result"]=1
				else:
					self.c.execute('''SELECT MAX(meetingNumber) FROM meetings
							WHERE meetingPrefix = :prefix 
						''',
						{"prefix": meetingPrefix})
					response["result"]=(self.c.fetchone()[0])

		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response

	def get_meeting_numbers_by_type(self, meetingPrefix):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				self.c.execute('''SELECT EXISTS(SELECT * FROM meetings
				WHERE meetingPrefix = :prefix) AS found
				''',
				{"prefix": meetingPrefix})
				if self.c.fetchone()[0]==0:
					response["status"]="No Records"
				else:
					self.c.execute('''SELECT meetingNumber FROM meetings
							WHERE meetingPrefix = :prefix 
						''',
						{"prefix": meetingPrefix})
					response["result"]=([_[0] for _ in self.c.fetchall()])

		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response

	def get_all_meeting_items_by_meeting(self, prefix, number):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				self.c.execute('''SELECT i.itemName, mis.statusActionsRequired, mis.statusPersonResponsible FROM items AS i
						JOIN meeting_item_status AS mis ON i.itemID = mis.itemID
						WHERE  mis.meetingPrefix= :prefix 
						AND mis.meetingNumber= :num
					''',
					{"prefix":prefix,
					"num":number})
				response["result"]=self.c.fetchall()


		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response

	def get_meeting_items_by_last_meeting(self, prefix, number):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				self.c.execute('''SELECT itemName FROM items
						JOIN meeting_item_status ON items.itemID = meeting_item_status.itemID
						WHERE  meeting_item_status.meetingPrefix= :prefix 
						AND meeting_item_status.meetingNumber= :num
					''',
					{"prefix":prefix,
					"num":number})
				response["result"]=[_[0] for _ in self.c.fetchall()]


		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response

	###################

	##Insert Statements##
	def insert_initial_records(self):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				currentMeetingTypes = [("M","MANCO"),
									("F","Finance"),
									("PTL","Project Team Leaders")]
				sql = "INSERT INTO meeting_types (meetingPrefix, meetingType) VALUES (?, ?)"
				self.c.executemany(sql,currentMeetingTypes)
				self.conn.commit()

				items = [("F","1"),
				("F","2"),
				("PTL","1")]
				sql = "INSERT INTO meetings (meetingPrefix, meetingNumber) VALUES (?, ?)"
				self.c.executemany(sql,items)
				self.conn.commit()

				items = [(1,"test1"),
						(2,"test2"),
						(3,"test3")]
				sql = "INSERT INTO items (itemID, itemName) VALUES (?, ?)"
				self.c.executemany(sql,items)
				self.conn.commit()

				items = [(1,1,"F","TBD", "TBD"),
						(2,2,"F", "TBD","TBD"),
						(3,1,"PTL", "TBD", "TBD")]
				sql = '''INSERT INTO meeting_item_status
				(itemID, meetingNumber, meetingPrefix, statusActionsRequired,statusPersonResponsible) 
				VALUES 
				(?, ?, ?, ?, ?)'''
				self.c.executemany(sql,items)
				self.conn.commit()
		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response

	def insert_meeting_item_statuses(self, itemList, prefix, number):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				for item in itemList:
					self.c.execute('''SELECT itemID FROM items
						WHERE itemName = :name
						''',
						{"name":item})
					itemID = self.c.fetchone()[0]
					self.c.execute('''INSERT INTO meeting_item_status
							(itemID, meetingNumber, meetingPrefix, statusActionsRequired, statusPersonResponsible) 
							VALUES 
							(:id, :num, :prefix, :actions, :person)''', 
							{"id":itemID, "num":number, "prefix":prefix, "actions":"TBD", "person":"TBD"})
					self.conn.commit()
		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response

	def insert_meeting(self, prefix, number):
		print(prefix, number)
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				self.c.execute('''INSERT INTO meetings
						(meetingPrefix, meetingNumber) 
						VALUES 
						(:prefix, :num)''', 
						{"prefix":prefix, "num":number})
				self.conn.commit()
		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response
	#####################

	##Update Statements##
	def update_meeting_item(self, item, prefix, number, action, person):
		response = {
		    "status":"Success",
		    "result":""
		}
		try:
			with self.conn:
				self.c.execute('''SELECT itemID FROM items
						WHERE itemName = :name
						''',
						{"name":item})
				itemID = self.c.fetchone()[0]
				self.c.execute('''UPDATE meeting_item_status SET
						statusActionsRequired = :actions, 
					    statusPersonResponsible = :person
					    WHERE itemID = :itemID
					    AND meetingNumber = :num
					    AND meetingPrefix = :prefix;
						''', 
						{"actions":action,
						"person":person,
						"itemID":itemID,
						"num":number,
						"prefix":prefix})
				self.conn.commit()
		except Exception as e:
			response["status"]="Error"
			response["result"]=e
		finally:
			return response
	#####################

	##Delete Statements##

	#####################

if __name__ == "__main__":
	dc = DatabaseConnector()
	print(dc.reinitialize_database())
	print(dc.get_meeting_types())
	input()






