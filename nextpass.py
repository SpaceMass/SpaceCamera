import ephem
import datetime
import time 
from time import gmtime, strftime
def get(x,y,iss):
	location = ephem.Observer()
	location.lon = x
	location.lat = y
	location.elevation = 2198
	timenow = datetime.datetime.utcnow()
	print timenow
	location.date = timenow
	#calculate where the ISS is
	re = location.next_pass(iss)
	next = re[1] - timenow
	print next
	return next


