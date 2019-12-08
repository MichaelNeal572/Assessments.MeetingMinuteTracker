import sqlite3

conn = sqlite3.connect('../Meeting Minutes.db')
c = conn.cursor()
try:
	with conn:
		c.execute('''UPDATE bugs 
			    		bugDetails = :details, 
					    bugArguments = :arguments, 
					    bugSource = :bugSource, 
					    bugDateCreated = :dateCreated, 
					    bugStatus = :status, 
					    bugExpectedResolution = :expectedResolution
					    WHERE rowid = :rowID
			    		''', 
			    		{"details":request.POST["bugDetails"],
			    		"arguments":request.POST["bugArguments"],
			    		"bugSource":request.POST["bugSource"],
			    		"dateCreated":request.POST["bugDateCreated"],
			    		"status":request.POST["bugStatus"],
			    		"expectedResolution":request.POST["bugExpectedResolution"],
			    		"rowID":request.POST["rowID"]})
    	conn.commit()