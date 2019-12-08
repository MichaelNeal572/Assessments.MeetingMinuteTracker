import sqlite3

conn = sqlite3.connect('../Meeting Minutes.db')
c = conn.cursor()
try:
	with conn:
		c.execute('''DELETE FROM devs 
			    WHERE rowid = :rowID
	    		''', 
	    		{"rowID":request.POST["rowID"]})