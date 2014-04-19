import nextpass
import ephem
import urllib2 #function for opening URLs
import urllib
boston = ephem.city('Boston')
data = urllib2.urlopen("http://www.celestrak.com/NORAD/elements/stations.txt")
stations_text_file = []
for line in data:
	stations_text_file.append(line)
iss = ephem.readtle(stations_text_file[0],
	stations_text_file[1],
	stations_text_file[2])
print(nextpass.get(boston.lat,boston.lon,iss))
