#!/usr/bin/python
#below are the imported modules for all of our operations
import sys #gives access to a variety of parameters and functions 
import math #function for mathematical operations
import ephem #function that gives locations of astronomical objects
import datetime
from time import gmtime, strftime #importing specific functions for time value 
import urllib2 #function for opening URLs
import xml.etree.ElementTree as ET #function to store our XML file data
try:
    # for Python2
    import Tkinter,tkFileDialog  #TKinter is Python's standard GUI package
    from Tkinter import *
except ImportError:
    # for Python3
    import tkinter,tkFileDialog
    from tkinter import *

import csv  #where csv = comma separated values --> format for spreadsheets and databases
#Code modified from http://stackoverflow.com/questions/1393324/in-python-given-a-url-to-a-text-file-what-is-the-simplest-way-to-read-the-cont
#More Code from http://www.icrar.org/__data/assets/pdf_file/0008/1436615/challenge09b-notes3.pdf
#We need to read the Two-line element set from http://www.celestrak.com/NORAD/elements/stations.txt
#below we are defining our global variables for our code
global filename 
filename = '' 
global testing
testing = ''
global locations
locations = []
global notes
notes =[]
data = urllib2.urlopen("http://www.celestrak.com/NORAD/elements/stations.txt")
stations_text_file = []
for line in data:
	stations_text_file.append(line)


#Code modified from http://brainwagon.org/2009/09/27/how-to-use-python-to-predict-satellite-locations/
#We need to extract the two line element for just the iss from http://www.celestrak.com/NORAD/elements/stations.txt
iss = ephem.readtle(stations_text_file[0],
	stations_text_file[1],
	stations_text_file[2])





#Create a new window 
window = Tkinter.Tk()
#draw the window, and start the 'application'

#Put a text widget in the main program
# Source: http://ygchan.blogspot.com/2012/05/python-how-to-make-clock-timer-in.html
#updating position of ISS based on website information: longitude, latitude, and a text box to hold that information
def positionupdater():
	timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	iss.compute(timenow)
	currentlong = iss.sublong 
	currentlat = iss.sublat 
	text_currentposition.configure(text="The Iss's Current Position is \n" + "Long:" + str(currentlong) + "\n" + "Lat:" + str(currentlat) +"\n")
	window.after(100, positionupdater)

#http://effbot.org/pyfaq/how-do-you-set-a-global-variable-in-a-function.htm
#setting a gloval variable in a function
def fileback():
	global filename
	from tkFileDialog import askopenfilename  
	Tk().withdraw() 
	filename = askopenfilename()
	fileread()

def fileread():
	global filename
	global testing
	global locations
	tree = ET.parse(filename)
	base = tree.getroot()
	#displays target locations extracted from XML file
	for elem in base.findall('EOSites/wmc__TEOSite'):
		print elem.get('Nomenclature'), elem.text
		location_storeage = elem.get('Nomenclature')
		locations.append(location_storeage)
	print(locations)
	text_file.configure(text="The Targets are: \n" + "\n".join(locations))

	#displays notes extracted from XML file
	for elem in base.findall('EOSites/wmc__TEOSite'):
		 print elem.get('Notes', elem.text)
		 notes_storeage = elem.get('Notes')
		 notes.append(notes_storeage)
	print(notes)
	notes_file.configure(text="The Notes are: \n" + "\n".join(notes))
	#text_file.configure(text=testing)

#Info about buttons http://effbot.org/tkinterbook/button.htm
#Parsing code from http://stackoverflow.com/questions/773797/updating-tkinter-labels-in-python
#settings for font, font size, pixel size, of the text in our GUI
timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
iss.compute(timenow)
currentlong = iss.sublong
currentlat = iss.sublat
text_currentposition = Tkinter.Label(window, text="", font=("Helvetica", 15))
text_currentposition.pack(anchor = "w", padx = 50, pady = 50)
text_file = Tkinter.Label(window, text="", font=("Helvetica", 15))
text_file.pack(anchor = "w", padx = 50, pady = 50)
notes_file = Tkinter.Label(window, text="", font=("Helvetica", 15))
notes_file.pack(anchor = "w", padx = 50, pady = 50)
b = Button(window, text="Browse for XML File", command=fileback)
b.pack()

positionupdater()
window.mainloop()

#TO RUN THE CODE AND SEE GUI, PLEASE SAVE AND THEN GO TO TOOLS --> BUILD


#obs = ephem.Observer()
#obs.lat = '40.6700'
#obs.long = '73.9400'
#for p in range(3):
#	tr, azr, tt, altt, ts, azs = obs.next_pass(iss)
#	while tr < ts :
#		obs.date = tr
#		iss.compute(obs)
#		print "%s %4.1f %5.1f" % (tr, math.degrees(iss.alt), math.degrees(iss.az))
#		tr = ephem.Date(tr + 60.0 * ephem.second)
#	print
#	obs.date = tr + ephem.minute
#this code is dope
