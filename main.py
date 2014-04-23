#!/usr/bin/python

#-----Begin Imports-----#

#below are the imported modules for all of our operations
import sys #gives access to a variety of parameters and functions 
import math #function for mathematical operations
import ephem #function that gives locations of astronomical objects
#importing specific functions for time value 
import datetime
import time 
from time import gmtime, strftime
import urllib2 #function for opening URLs
import urllib
import cStringIO
import xml.etree.ElementTree as ET #function to store our XML file data
try:
    # for Python2
    import Tkinter,tkFileDialog  #TKinter is Python's standard GUI package
    from Tkinter import *
except ImportError:
    # for Python3
    import tkinter,tkFileDialog
    from tkinter import *
import PIL
from PIL import Image
from PIL import ImageTk
import csv  #where csv = comma separated values --> format for spreadsheets and databases
#Code modified from http://stackoverflow.com/questions/1393324/in-python-given-a-url-to-a-text-file-what-is-the-simplest-way-to-read-the-cont
#More Code from http://www.icrar.org/__data/assets/pdf_file/0008/1436615/challenge09b-notes3.pdf
#We need to read the Two-line element set from http://www.celestrak.com/NORAD/elements/stations.txt
#below we are defining our global variables for our code
import StringIO
import cStringIO, base64
import nextpass
#-----End Imports-----#


#-----Begin Global Declarations-----#
global filename 
filename = ''
#Import base64 for converting gif into binary  
import base64
global testing
testing = ''
global locations
locations = []
global notes
notes =[]
#data = urllib2.urlopen("http://www.celestrak.com/NORAD/elements/stations.txt")
stations_text_file = []
#for line in data:
#	stations_text_file.append(line)
global EOSites_store
EOSites_store = []
global currentlongfloat
currentlongfloat = 0.001
global currentlatfloat
currentlatfloat = 0.001
global futureonoff
futureonoff = True
#-----End Global Declarations-----#



#Code modified from http://brainwagon.org/2009/09/27/how-to-use-python-to-predict-satellite-locations/
#We need to extract the two line element for just the iss from http://www.celestrak.com/NORAD/elements/stations.txt
iss = ephem.readtle('ISS',
	'1 25544U 98067A   14097.76250877  .00016717  00000-0  10270-3 0  9000',
	'2 25544  51.6480  88.5903 0002624 354.6196   5.4926 15.50582954   401')





#Create a new window 
window = Tkinter.Tk()
window.wm_title("SpaceMass")
window.self= Text(bg='black')
window.self.pack(fill="both", expand=True)
def center_window(w=1000, h=1000):
	ws = window.winfo_screenwidth()
	hs = window.winfo_screenheight()
	#calculate position x,y
	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))
center_window(1000, 775)

#draw the window, and start the 'application'

timetoadd=5
timenow = datetime.datetime.utcnow()
iss.compute(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
global long_list_3_orbits
long_list_3_orbits = []
global lat_list_3_orbits
lat_list_3_orbits = []
while timetoadd < 90*2:
	#print(timenow + datetime.timedelta(0,timetoadd*60))
	#print(timenow)
	iss.compute(timenow + datetime.timedelta(0,timetoadd*60))
	long_list_3_orbits.append(round(float(iss.sublong)*57.2957795,3))
	lat_list_3_orbits.append(round(float(iss.sublat)*57.2957795,3))
	timetoadd = timetoadd + 5
	#print(iss.sublong)
	#print(iss.sublat)
	#print(timetoadd)
#print(long_list_3_orbits)
#print(lat_list_3_orbits)

#create a target information window for first location
def newpage1():
	win=Toplevel()
	message = "Target Information"
	Label(win, text=message).pack()
	close = Button(win,text='Close', command=win.destroy,font=("Helvetica", 15))
	close.pack()
	close.place(x=450,y=650)
	win.wm_title("SpaceMass")
	win.geometry("1000x1000")
#map for first target location 
	toopen = get_static_google_map("image2", center=data_from_xml[6][0]+","+data_from_xml[7][0], zoom=8, imgsize=(500,500), imgformat="gif", maptype="satellite")
	#Code from http://stackoverflow.com/questions/6086262/python-3-how-to-retrieve-an-image-from-the-web-and-display-in-a-gui-using-tkint
	# from http://www.daniweb.com/software-development/python/threads/79337/putting-an-image-into-a-tkinter-thingy
	# pick an image file you have .bmp  .jpg  .gif.  .png
	# load the file and covert it to a Tkinter image object
	u = urllib.urlopen(toopen)
	raw_data = u.read()
	u.close()
	b64_data = base64.encodestring(raw_data)
	imgtoprint = Tkinter.PhotoImage(data=b64_data)

	imagebox = Tkinter.Label(win, image=imgtoprint)
	imagebox.image = imgtoprint
	imagebox.pack()


#key information for first target location
	text_locationname = Tkinter.Label(win, text="", font=("Helvetica", 25))
	text_locationname.pack(anchor = "w", padx = 50)
	text_locationname.place(x=400,y=50)
	text_locationname.configure(text=data_from_xml[0][0])

	text_passingtime = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_passingtime.pack(anchor = "w", padx = 50)
	text_passingtime.place(x=50,y=500)
	text_passingtime.configure(text= "Time of Next Pass: " + data_from_xml[1][0])

	text_longlat = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_longlat.pack(anchor = "w", padx = 50)
	text_longlat.place(x=50,y=525)
	text_longlat.configure(text= "Location of Target: " + data_from_xml[5][0])

	text_weather = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_weather.pack(anchor = "w", padx = 50)
	text_weather.place(x=50,y=550)
	text_weather.configure(text= "Weather Conditions: " + data_from_xml[3][0])

	text_lenstype = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_lenstype.pack(anchor = "w", padx = 50)
	text_lenstype.place(x=50,y=600)
	text_lenstype.configure(text= "Lens Type: " + data_from_xml[2][0])

	text_nadir = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_nadir.pack(anchor = "w", padx = 50)
	text_nadir.place(x=50,y=625)
	text_nadir.configure(text=data_from_xml[4][0])





	#image1.configure(file='mymap2.jpg')

#create a target information window for second location
def newpage2():
	win=Toplevel()
	message = "Target Information"
	Label(win, text=message).pack()
	close = Button(win,text='Close', command=win.destroy,font=("Helvetica", 15))
	close.pack()
	close.place(x=450,y=650)
	win.wm_title("SpaceMass")
	win.geometry("1000x1000")

#map for first target location 
	toopen = get_static_google_map("image2", center=data_from_xml[6][1]+","+data_from_xml[7][1], zoom=8, imgsize=(500,500), imgformat="gif", maptype="satellite")
	#Code from http://stackoverflow.com/questions/6086262/python-3-how-to-retrieve-an-image-from-the-web-and-display-in-a-gui-using-tkint
	# from http://www.daniweb.com/software-development/python/threads/79337/putting-an-image-into-a-tkinter-thingy
	# pick an image file you have .bmp  .jpg  .gif.  .png
	# load the file and covert it to a Tkinter image object
	u = urllib.urlopen(toopen)
	raw_data = u.read()
	u.close()
	b64_data = base64.encodestring(raw_data)
	imgtoprint = Tkinter.PhotoImage(data=b64_data)

	imagebox = Tkinter.Label(win, image=imgtoprint)
	imagebox.image = imgtoprint
	imagebox.pack()
	imagebox.place(relx=0.25, rely=0.38, anchor=CENTER)

#key info for second target location
	text_locationname2 = Tkinter.Label(win, text="", font=("Helvetica", 25))
	text_locationname2.pack(anchor = "w", padx = 50)
	text_locationname2.place(relx=0.5,rely=0.06, anchor=CENTER)
	text_locationname2.configure(text=data_from_xml[0][1])

	text_passingtime2 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_passingtime2.pack(anchor = "w", padx = 50)
	text_passingtime2.place(x=50,y=500)
	text_passingtime2.configure(text= "TIME OF NEXT PASS: " + data_from_xml[1][1])

	text_longlat2 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_longlat2.pack(anchor = "w", padx = 50)
	text_longlat2.place(x=50,y=525)
	text_longlat2.configure(text= "Location of Target: " + data_from_xml[5][1])

	text_weather2 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_weather2.pack(anchor = "w", padx = 50)
	text_weather2.place(x=50,y=550)
	text_weather2.configure(text="Weather Conditions: " + data_from_xml[3][1])

	text_lenstype2 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_lenstype2.pack(anchor = "w", padx = 50)
	text_lenstype2.place(x=50,y=600)
	text_lenstype2.configure(text= "Lens Type: " + data_from_xml[2][1])

	text_nadir2 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_nadir2.pack(anchor = "w", padx = 50)
	text_nadir2.place(x=50,y=625)
	text_nadir2.configure(text=data_from_xml[4][1])

#create a target information window for third location
def newpage3():
	win=Toplevel()
	message = "Target Information"
	Label(win, text=message).pack()
	close = Button(win,text='Close', command=win.destroy,font=("Helvetica", 15))
	close.pack()
	close.place(x=450,y=650)
	win.wm_title("SpaceMass")
	win.geometry("1000x1000")

#map for third target location
	toopen = get_static_google_map("image2", center=data_from_xml[6][2]+","+data_from_xml[7][2], zoom=8, imgsize=(500,500), imgformat="gif", maptype="satellite")
	#Code from http://stackoverflow.com/questions/6086262/python-3-how-to-retrieve-an-image-from-the-web-and-display-in-a-gui-using-tkint
	# from http://www.daniweb.com/software-development/python/threads/79337/putting-an-image-into-a-tkinter-thingy
	# pick an image file you have .bmp  .jpg  .gif.  .png
	# load the file and covert it to a Tkinter image object
	u = urllib.urlopen(toopen)
	raw_data = u.read()
	u.close()
	b64_data = base64.encodestring(raw_data)
	imgtoprint = Tkinter.PhotoImage(data=b64_data)

	imagebox = Tkinter.Label(win, image=imgtoprint)
	imagebox.image = imgtoprint
	imagebox.pack()

#key info for third target location
	text_locationname3 = Tkinter.Label(win, text="", font=("Helvetica", 25))
	text_locationname3.pack(anchor = "w", padx = 50)
	text_locationname3.place(x=400,y=50)
	text_locationname3.configure(text=data_from_xml[0][2])

	text_passingtime3 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_passingtime3.pack(anchor = "w", padx = 50)
	text_passingtime3.place(x=50,y=500)
	text_passingtime3.configure(text= "Time of Next Pass: " + data_from_xml[1][2])

	text_longlat3 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_longlat3.pack(anchor = "w", padx = 50)
	text_longlat3.place(x=50,y=525)
	text_longlat3.configure(text= "Location of Target: " + data_from_xml[5][2])

	text_weather3 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_weather3.pack(anchor = "w", padx = 50)
	text_weather3.place(x=50,y=550)
	text_weather3.configure(text="Weather Conditions: " + data_from_xml[3][2])

	text_lenstype3 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_lenstype3.pack(anchor = "w", padx = 50)
	text_lenstype3.place(x=50,y=600)
	text_lenstype3.configure(text= "Lens Type: " + data_from_xml[2][2])

	text_nadir3 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_nadir3.pack(anchor = "w", padx = 50)
	text_nadir3.place(x=50,y=625)
	text_nadir3.configure(text=data_from_xml[4][2])

#create a target information window for fourth location
def newpage4():
	win=Toplevel()
	message = "Target Information"
	Label(win, text=message).pack()
	close = Button(win,text='Close', command=win.destroy,font=("Helvetica", 15))
	close.pack()
	close.place(x=450,y=650)
	win.wm_title("SpaceMass")
	win.geometry("1000x1000")

#map for fourth target location
	toopen = get_static_google_map("image2", center=data_from_xml[6][3]+","+data_from_xml[7][3], zoom=8, imgsize=(500,500), imgformat="gif", maptype="satellite")
	#Code from http://stackoverflow.com/questions/6086262/python-3-how-to-retrieve-an-image-from-the-web-and-display-in-a-gui-using-tkint
	# from http://www.daniweb.com/software-development/python/threads/79337/putting-an-image-into-a-tkinter-thingy
	# pick an image file you have .bmp  .jpg  .gif.  .png
	# load the file and covert it to a Tkinter image object
	u = urllib.urlopen(toopen)
	raw_data = u.read()
	u.close()
	b64_data = base64.encodestring(raw_data)
	imgtoprint = Tkinter.PhotoImage(data=b64_data)

	imagebox = Tkinter.Label(win, image=imgtoprint)
	imagebox.image = imgtoprint
	imagebox.pack()

#key info for fourth target location
	text_locationname4 = Tkinter.Label(win, text="", font=("Helvetica", 25))
	text_locationname4.pack(anchor = "w", padx = 50)
	text_locationname4.place(x=400,y=50)
	text_locationname4.configure(text=data_from_xml[0][3])

	text_passingtime4 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_passingtime4.pack(anchor = "w", padx = 50)
	text_passingtime4.place(x=50,y=500)
	text_passingtime4.configure(text= "Time of Next Pass: " + data_from_xml[1][3])

	text_longlat4 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_longlat4.pack(anchor = "w", padx = 50)
	text_longlat4.place(x=50,y=525)
	text_longlat4.configure(text= "Location of Target: " + data_from_xml[5][3])

	text_weather4 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_weather4.pack(anchor = "w", padx = 50)
	text_weather4.place(x=50,y=550)
	text_weather4.configure(text="Weather Conditions: " + data_from_xml[3][3])

	text_lenstype4 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_lenstype4.pack(anchor = "w", padx = 50)
	text_lenstype4.place(x=50,y=600)
	text_lenstype4.configure(text= "Lens Type: " + data_from_xml[2][3])

	text_nadir4 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_nadir4.pack(anchor = "w", padx = 50)
	text_nadir4.place(x=50,y=625)
	text_nadir4.configure(text=data_from_xml[4][3])

#create a target information window for fifth location
def newpage5():
	win=Toplevel()
	message = "Target Information"
	Label(win, text=message).pack()
	close = Button(win,text='Close', command=win.destroy,font=("Helvetica", 15))
	close.pack()
	close.place(x=450,y=650)
	win.wm_title("SpaceMass")
	win.geometry("1000x1000")

#map for fifth target location 
	toopen = get_static_google_map("image2", center=data_from_xml[6][4]+","+data_from_xml[7][4], zoom=8, imgsize=(500,500), imgformat="gif", maptype="satellite")
	#Code from http://stackoverflow.com/questions/6086262/python-3-how-to-retrieve-an-image-from-the-web-and-display-in-a-gui-using-tkint
	# from http://www.daniweb.com/software-development/python/threads/79337/putting-an-image-into-a-tkinter-thingy
	# pick an image file you have .bmp  .jpg  .gif.  .png
	# load the file and covert it to a Tkinter image object
	u = urllib.urlopen(toopen)
	raw_data = u.read()
	u.close()
	b64_data = base64.encodestring(raw_data)
	imgtoprint = Tkinter.PhotoImage(data=b64_data)

	imagebox = Tkinter.Label(win, image=imgtoprint)
	imagebox.image = imgtoprint
	imagebox.pack()

#key info for fifth target location
	text_locationname5 = Tkinter.Label(win, text="", font=("Helvetica", 25))
	text_locationname5.pack(anchor = "w", padx = 50)
	text_locationname5.place(x=400,y=50)
	text_locationname5.configure(text=data_from_xml[0][4])

	text_passingtime5 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_passingtime5.pack(anchor = "w", padx = 50)
	text_passingtime5.place(x=50,y=500)
	text_passingtime5.configure(text= "Time of Next Pass: " + data_from_xml[1][4])

	text_longlat5 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_longlat5.pack(anchor = "w", padx = 50)
	text_longlat5.place(x=50,y=525)
	text_longlat5.configure(text= "Location of Target: " + data_from_xml[5][4])

	text_weather5 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_weather5.pack(anchor = "w", padx = 50)
	text_weather5.place(x=50,y=550)
	text_weather5.configure(text="Weather Conditions: " + data_from_xml[3][4])

	text_lenstype5 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_lenstype5.pack(anchor = "w", padx = 50)
	text_lenstype5.place(x=50,y=600)
	text_lenstype5.configure(text= "Lens Type: " + data_from_xml[2][4])

	text_nadir5 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_nadir5.pack(anchor = "w", padx = 50)
	text_nadir5.place(x=50,y=625)
	text_nadir5.configure(text=data_from_xml[4][4])

#create a target information window for sixth location
def newpage6():
	win=Toplevel()
	message = "Target Information"
	Label(win, text=message).pack()
	close = Button(win,text='Close', command=win.destroy,font=("Helvetica", 15))
	close.pack()
	close.place(x=450,y=650)
	win.wm_title("SpaceMass")
	win.geometry("1000x1000")

#map for sixth target location 
	toopen = get_static_google_map("image2", center=data_from_xml[6][5]+","+data_from_xml[7][5], zoom=8, imgsize=(500,500), imgformat="gif", maptype="satellite")
	#Code from http://stackoverflow.com/questions/6086262/python-3-how-to-retrieve-an-image-from-the-web-and-display-in-a-gui-using-tkint
	# from http://www.daniweb.com/software-development/python/threads/79337/putting-an-image-into-a-tkinter-thingy
	# pick an image file you have .bmp  .jpg  .gif.  .png
	# load the file and covert it to a Tkinter image object
	u = urllib.urlopen(toopen)
	raw_data = u.read()
	u.close()
	b64_data = base64.encodestring(raw_data)
	imgtoprint = Tkinter.PhotoImage(data=b64_data)

	imagebox = Tkinter.Label(win, image=imgtoprint)
	imagebox.image = imgtoprint
	imagebox.pack()

#key info for sixth target location
	text_locationname6 = Tkinter.Label(win, text="", font=("Helvetica", 25))
	text_locationname6.pack(anchor = "w", padx = 50)
	text_locationname6.place(x=400,y=50)
	text_locationname6.configure(text=data_from_xml[0][5])

	text_passingtime6 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_passingtime6.pack(anchor = "w", padx = 50)
	text_passingtime6.place(x=50,y=500)
	text_passingtime6.configure(text= "Time of Next Pass: " + data_from_xml[1][5])

	text_longlat6 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_longlat6.pack(anchor = "w", padx = 50)
	text_longlat6.place(x=50,y=525)
	text_longlat6.configure(text= "Location of Target: " + data_from_xml[5][5])

	text_weather6 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_weather6.pack(anchor = "w", padx = 50)
	text_weather6.place(x=50,y=550)
	text_weather6.configure(text="Weather Conditions: " + data_from_xml[3][2])

	text_lenstype6 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_lenstype6.pack(anchor = "w", padx = 50)
	text_lenstype6.place(x=50,y=600)
	text_lenstype6.configure(text= "Lens Type: " + data_from_xml[2][5])

	text_nadir6 = Tkinter.Label(win, text="", font=("Helvetica", 15))
	text_nadir6.pack(anchor = "w", padx = 50)
	text_nadir6.place(x=50,y=625)
	text_nadir6.configure(text=data_from_xml[4][5])

#Make a global variable that will hold the list of markers we want to put on the map
#credit to http://hci574.blogspot.com/2010/04/using-google-maps-static-images.html
global marker_list
marker_list = []

#Put a text widget in the main program
# Source: http://ygchan.blogspot.com/2012/05/python-how-to-make-clock-timer-in.html
#updating position of ISS based on website information: longitude, latitude, and a text box to hold that information
def positionupdater():
	timenow = strftime("%Y-%m-%d", gmtime())
	datenow = strftime("%H:%M:%S", gmtime())
	timenowforcomputing = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	iss.compute(timenowforcomputing)
	currentlong = iss.sublong 
	currentlat = iss.sublat 
	#google maps only takes degrees, however Pyemphem can gives out Astronamical formate or radians. Let's get the radians. 
	currentlongfloat= float(iss.sublong)
	currentlatfloat= float(iss.sublat)
	#convert radians to degrees with the equations 1 radian = 57.2957795 degrees
	#TODO Learn how to use pi in python 
	currentlongfloat = currentlongfloat*57.2957795
	currentlatfloat= currentlatfloat*57.2957795
	#print(currentlongfloat)
	#print(currentlatfloat)
	#update the world map with the current location
	text_currentposition.configure(text="The Iss's Current Position is \n" + "Long:" + str(currentlong) + "\n" + "Lat:" + str(currentlat) +"\n")
	text_currentposition.place(relx=0.3,rely=0.2, anchor=CENTER)
	text_clock.configure(text="Date: " + str(timenow) + "   Time: " + str(datenow))
	#TODO split the clock thread and the map thread. We need to slow down the clock to get the google API to work, but now the clock counts slow
	window.after(1000, positionupdater)
def buttonclock():
	text_position1.configure(text=data_from_xml[0][0] + " in " + nextpass.get(data_from_xml[6][0],data_from_xml[7][0],iss))
	text_position2.configure(text=data_from_xml[0][1] + " in " + nextpass.get(data_from_xml[6][1],data_from_xml[7][1],iss))
	text_position3.configure(text=data_from_xml[0][2] + " in " + nextpass.get(data_from_xml[6][2],data_from_xml[7][2],iss))
	text_position4.configure(text=data_from_xml[0][3] + " in " + nextpass.get(data_from_xml[6][3],data_from_xml[7][3],iss))
	text_position5.configure(text=data_from_xml[0][4] + " in " + nextpass.get(data_from_xml[6][4],data_from_xml[7][4],iss))
	text_position6.configure(text=data_from_xml[0][5] + " in " + nextpass.get(data_from_xml[6][5],data_from_xml[7][5],iss))
	window.after(1000, buttonclock)

#updating map based on ISS location
def mapupdater():
	global futureonoff
	marker_list = []
	timenowforcomputing = strftime("%Y-%m-%d %H:%M:%S", gmtime())
	iss.compute(timenowforcomputing)
	currentlong = iss.sublong 
	currentlat = iss.sublat 
	currentlongfloat= float(iss.sublong)
	currentlatfloat= float(iss.sublat)
	#convert radians to degrees with the equations 1 radian = 57.2957795 degrees
	#TODO Learn how to use pi in python 
	currentlongfloat = round(currentlongfloat*57.2957795, 3)
	currentlatfloat= round(currentlatfloat*57.2957795, 3)
	print(currentlongfloat)
	print(currentlatfloat)
	if futureonoff == True:
		futureintermenter = 0
		while futureintermenter < len(long_list_3_orbits):
			marker_list.append("markers=size:mid|label:F|color:blue|"+str(lat_list_3_orbits[futureintermenter])+","+str(long_list_3_orbits[futureintermenter])+"|")
			futureintermenter = futureintermenter + 1
	marker_list.append("markers=size:mid|label:S|color:red|"+str(currentlatfloat)+","+str(currentlongfloat)+"|")
	toopenupdater = get_static_google_map("mymap2", center="42.950827,-122.108974", zoom=1, imgsize=(500,500), imgformat="gif", maptype="satellite", markers=marker_list)
	#print(toopenupdater)
	#Code from http://stackoverflow.com/questions/6086262/python-3-how-to-retrieve-an-image-from-the-web-and-display-in-a-gui-using-tkint
	#im = PIL.Image.open("mymap2.png")
	uupdater = urllib.urlopen(toopenupdater)
	raw_data_u = uupdater.read()
	u.close()
	b64_data_u = base64.encodestring(raw_data_u)
	imgtoprint = Tkinter.PhotoImage(data=b64_data)

	# from http://www.daniweb.com/software-development/python/threads/79337/putting-an-image-into-a-tkinter-thingy
	# pick an image file you have .bmp  .jpg  .gif.  .png
	# load the file and covert it to a Tkinter image object
	#imageFile = "mymap2.png"
	#image1 = ImageTk.PhotoImage(Image.open(imageFile))
	#image1.configure(file='mymap2.jpg')
	panel1.configure(image = imgtoprint)
	panel1.image = imgtoprint
	#updata map after 30 seconds
	window.after(30000, mapupdater)









#background code for map
def get_static_google_map(filename_wo_extension, center=None, zoom=None, imgsize="500x500", imgformat="gif",
                          maptype="roadmap", markers=None ):  
    """retrieve a map (image) from the static google maps server 
    
     See: http://code.google.com/apis/maps/documentation/staticmaps/
        
        Creates a request string with a URL like this:
        http://maps.google.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=14&size=512x512&maptype=roadmap
&markers=color:blue|label:S|40.702147,-74.015794&sensor=false"""
   
    
    # assemble the URL
    request =  "http://maps.google.com/maps/api/staticmap?" # base URL, append query params, separated by &
   
    # if center and zoom  are not given, the map will show all marker locations
    if center != None:
        request += "center=%s&" % center
        #request += "center=%s&" % "40.714728, -73.998672"   # latitude and longitude (up to 6-digits)
        #request += "center=%s&" % "50011" # could also be a zipcode,
        #request += "center=%s&" % "Brooklyn+Bridge,New+York,NY"  # or a search term 
    if center != None:
        request += "zoom=%i&" % zoom  # zoom 0 (all of the world scale ) to 22 (single buildings scale)


    request += "size=%ix%i&" % (imgsize)  # tuple of ints, up to 640 by 640
    request += "format=%s&" % imgformat
    request += "maptype=%s&" % maptype  # roadmap, satellite, hybrid, terrain


    # add markers (location and style)
    if markers != None:
        for marker in markers:
                request += "%s&" % marker


    #request += "mobile=false&"  # optional: mobile=true will assume the image is shown on a small screen (mobile device)
    request += "sensor=false&"   # must be given, deals with getting loction from mobile device 
    print request
    return request

    
def togglemap():
	global futureonoff
	print(futureonoff)
	if futureonoff == True:
		futureonoff = False
	else:
		futureonoff = True
	mapupdater()
	print(futureonoff)
#setting a global variable in a function
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
	Nomenclature_Increment = 0
	global locations_list
	locations_list = []
	for elem in base.findall('EOSites/wmc__TEOSite'):
		#print elem.get('Nomenclature'), elem.text
		location_storeage = elem.get('Nomenclature')
		locations.append(location_storeage)
		locations_list.append(location_storeage)
	#print(locations)
	#print(locations_list)


	#displays notes extracted from XML file
	global GMT
	GMT = []
	global Lens
	Lens = []
	global weather
	weather = []
	global nadir_true_false
	nadir_true_false = []
	global track 
	track = []
	global targetlat
	targetlat = []
	global targetlong
	targetlong = []
	global data_from_xml
	data_from_xml = []
	global risetime
	risetime = []
	global riseazimuth
	riseazimuth = []
	global settime
	settime = []
	global setazimuth
	setazimuth = []
	for elem in base.findall('EOSites/wmc__TEOSite'):
		weather_string = ''
		#print elem.get('Notes', elem.text)
		notes_storeage = elem.get('Notes')
		#Find the location of the GMT information to split the string at that location
		GMT_index = notes_storeage.index('GMT')
		GMT.append(notes_storeage[GMT_index+5]+notes_storeage[GMT_index+6]+notes_storeage[GMT_index+7]+notes_storeage[GMT_index+8]+notes_storeage[GMT_index+9]+notes_storeage[GMT_index+10]+notes_storeage[GMT_index+11]+notes_storeage[GMT_index+12])
		#Find the location of the lens information to split the string at that location
		Lens_index = notes_storeage.index('Lens')
		Lens.append(notes_storeage[Lens_index+10]+notes_storeage[Lens_index+11]+notes_storeage[Lens_index+12]+notes_storeage[Lens_index+13]+notes_storeage[Lens_index+14]+notes_storeage[Lens_index+15]+notes_storeage[Lens_index+16]+notes_storeage[Lens_index+17])
		if 'early morning' in notes_storeage:
			weather_string = weather_string + 'The pass will take place during Early Morning Local Time'
		if 'mid-morning' in notes_storeage:
		 	weather_string = weather_string + 'The pass will take place during Mid-morning local time'
		if 'clear' in notes_storeage:
		 	weather_string = weather_string + " Cloud conditions are clear"		
		if 'partly cloudy' in notes_storeage:
		 	weather_string = weather_string + " Cloud conditions are partly cloudy"
		weather.append(weather_string)
		nadir_true_false.append('nadir' in notes_storeage)
		if 'left of track' in notes_storeage:
			track.append('left of track')
		if 'right of track' in notes_storeage:
			track.append('right of track')
		if 'Closest approach' in notes_storeage:
			track_index = notes_storeage.index('Closest')
			z = 17
			z_str = ''
			while (z < (len(notes_storeage)-track_index)):
				z_str = z_str + notes_storeage[track_index+z]
				z = z + 1
			track.append(z_str)
	for elem in base.findall('EOSites/wmc__TEOSite/TGeoCoordsEx'):
		lat_storage=elem.get('lat')
		#I have the data, but it is in radians, convert to degrees for google
		#convert radians to degrees with the equations 1 radian = 57.2957795 degrees
		lat_storage= str(float(lat_storage)*57.2957795)
		targetlat.append(lat_storage)
		long_storage=elem.get('lon')
		long_storage= str(float(long_storage)*57.2957795)
		targetlong.append(long_storage)
		timingdata = nextpass.full(lat_storage,long_storage,iss)
		risetime.append(timingdata[0])
		riseazimuth.append(timingdata[1])
		settime.append(timingdata[2])
		#setazimuth(timingdata[3])
		print(timingdata)
		print(lat_storage)
		print(long_storage)


	data_from_xml.append(locations_list)
	data_from_xml.append(GMT)
	data_from_xml.append(Lens)
	data_from_xml.append(weather)
	data_from_xml.append(nadir_true_false)
	data_from_xml.append(track)
	data_from_xml.append(targetlat)
	data_from_xml.append(targetlong)
	data_from_xml.append(risetime)
	data_from_xml.append(riseazimuth)
	data_from_xml.append(settime)
	data_from_xml.append(setazimuth)
	print(targetlat)
	print(targetlong)
	print(timingdata)
	#print(notes)
	#print(Lens)
	#print(weather)
	#print(nadir_true_false)
	#print(targetlong)
	#print(targetlat)
	#print(data_from_xml[0][1])


	#creating the buttons for each one of the locations, each button brings up a new page with target info
	global text_position1
	global text_position2
	global text_position3
	global text_position4
	global text_position5
	global text_position6

	text_position1 = Button(window, text="", font=("Helvetica", 15), command=newpage1)
	text_position1.pack(anchor = "w", padx = 50)
	text_position1.place(x=50,y=350)
	text_position2 = Button(window, text="", font=("Helvetica", 15), command=newpage2)
	text_position2.pack(anchor = "w", padx = 50)
	text_position2.place(x=50,y=400)
	text_position3 = Button(window, text="", font=("Helvetica", 15), command=newpage3)
	text_position3.pack(anchor = "w", padx = 50)
	text_position3.place(x=50,y=450)
	text_position4 = Button(window, text="", font=("Helvetica", 15), command=newpage4)
	text_position4.pack(anchor = "w", padx = 50)
	text_position4.place(x=50,y=500)
	text_position5 = Button(window, text="", font=("Helvetica", 15), command=newpage5)
	text_position5.pack(anchor = "w", padx = 50)
	text_position5.place(x=50,y=550)
	text_position6 = Button(window, text="", font=("Helvetica", 15), command=newpage6)
	text_position6.pack(anchor = "w", padx = 50)
	text_position6.place(x=50,y=600)

	text_todaystargets = Tkinter.Label(window, text="Today's Targets", font=("Helvetica", 15), bg='light blue')
	text_todaystargets.pack(anchor = "w", padx = 50)
	text_todaystargets.place(x=50,y=300)

	text_position1.configure(text=data_from_xml[0][0])
	text_position2.configure(text=data_from_xml[0][1])
	text_position3.configure(text=data_from_xml[0][2])
	text_position4.configure(text=data_from_xml[0][3])
	text_position5.configure(text=data_from_xml[0][4])
	text_position6.configure(text=data_from_xml[0][5])
	buttonclock()

	#text_file.configure(text=testing)
#Info about buttons http://effbot.org/tkinterbook/button.htm
#Parsing code from http://stackoverflow.com/questions/773797/updating-tkinter-labels-in-python
#settings for font, font size, pixel size, of the text in our GUI
timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
iss.compute(timenow)
currentlong = iss.sublong
currentlat = iss.sublat
text_currentposition = Tkinter.Label(window, text="", font=("Helvetica", 15), bg='black', fg='white')#clock
text_currentposition.pack(anchor = "w", padx = 50)#clock
text_clock = Tkinter.Label(window, text="", font=("Helvetica", 25), bg = 'black', fg= 'white')
text_clock.pack(anchor = "w", padx = 50)
text_clock.place(relx=0.5,rely=0.05, anchor=CENTER)
marker_list = []
timenowforcomputing = strftime("%Y-%m-%d %H:%M:%S", gmtime())
iss.compute(timenowforcomputing)
currentlong = iss.sublong 
currentlat = iss.sublat 
currentlongfloat= float(iss.sublong)
currentlatfloat= float(iss.sublat)
#convert radians to degrees with the equations 1 radian = 57.2957795 degrees
#TODO Learn how to use pi in python 
currentlongfloat = round(currentlongfloat*57.2957795, 3)
currentlatfloat= round(currentlatfloat*57.2957795, 3)
if futureonoff == True:
	futureintermenter = 0
	while futureintermenter < len(long_list_3_orbits):
		marker_list.append("markers=size:mid|label:F|color:blue|"+str(lat_list_3_orbits[futureintermenter])+","+str(long_list_3_orbits[futureintermenter])+"|")
		futureintermenter = futureintermenter + 1
marker_list.append("markers=size:mid|label:S|color:red|"+str(currentlatfloat)+","+str(currentlongfloat)+"|")
#places map into GUI
toopen = get_static_google_map("mymap2", center="42.950827,-122.108974", zoom=1, imgsize=(500,500), imgformat="gif", maptype="satellite", markers=marker_list)
#im = PIL.Image.open("mymap2.png")
#imageFile = "mymap2.png"
#Code from http://stackoverflow.com/questions/6086262/python-3-how-to-retrieve-an-image-from-the-web-and-display-in-a-gui-using-tkint
#print(toopen)
u = urllib.urlopen(toopen)
raw_data = u.read()
u.close()
b64_data = base64.encodestring(raw_data)
global imgtoprint
imgtoprint = Tkinter.PhotoImage(data=b64_data)
panel1 = Tkinter.Label(window, image=imgtoprint, bg='black', width = 500, height = 400)
panel1.pack(side='top', fill='both', expand='yes',anchor = "w", padx = 50)
panel1.place(relx=0.3,rely=0.5, anchor=CENTER)
b = Button(window, text="Browse for XML File", font=("Helvetica", 15), command=fileback, bg = 'white')
b.pack()
b.place(relx=0.5,rely=0.9, anchor=CENTER)
c = Button(window, text="Toggle Orbit Prediction on Map", font=("Helvetica", 15), command=togglemap, bg = 'black')
c.pack()
c.place(x=425,y=850)

positionupdater()
mapupdater()
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
