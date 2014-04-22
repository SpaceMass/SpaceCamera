import ephem
import datetime
from datetime import datetime, timedelta
import time 
from time import gmtime, strftime
def get(x,y,iss):
	#Lat, long, iss
	location = ephem.Observer()
	location.lat = x
	location.lon = y
	location.elevation = 2198
	timenow = datetime.utcnow()
	#print timenow
	location.date = timenow
	#calculate where the ISS is
	nextpassdata = location.next_pass(iss)
	try: 
		next = nextpassdata[0] - ephem.Date(timenow)
		timeseconds = next*86400
		timeseconds = timedelta(seconds=timeseconds)
		d = datetime(1,1,1) + timeseconds
		returner = "%d:%d:%d" % (d.hour, d.minute, d.second)
	except: 
		returner = "LOS"
	#print "This is the nextpassdata array " 
	#print nextpassdata
	#print "This is the rise time " + str(nextpassdata[0])
	#print "This is the current time in emphem format " + str(ephem.Date(timenow))
	#print next
	#print "this is the time remaining in seconds"
	#print timeseconds
	#Code from http://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
	#print ("%d:%d:%d" % (d.hour, d.minute, d.second))
	return returner
