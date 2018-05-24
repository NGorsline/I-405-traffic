import numpy as np
import car_agent
np.set_printoptions(threshold=np.inf)
import math
import tkinter
import matplotlib.pyplot as plt
import matplotlib.colors
import time

global freeway
global TIME_SECONDS
global TOL_COUNT
global REG_COUNT

#CONSTANTS
#---------
#Represents regular lanes in the freeway
REGULAR = 1
#Represents the off ramp on the freeway
OFF_RAMP = 2
#Represents the toll lane on the freeway
TOLL = 3
#Represents the on ramp on the freeway
ON_RAMP = 4
#Represents the total lanes on the freeway
LANES = 4
#Represents locations of the freeway where a car is not allowed to drive in
NOT_USED = -1
#Represents the total number of indexes we need to represent 6.8 miles.
#Each index represent 15 feet.

MILES = 2320 
#Represents the dotted lines
CAN_CHANGE_LANES = True
#Represents double white lines 
CANNOT_CHANGE_LANES = False 
TIME_SECONDS = 0
TOL_COUNT = 0
REG_COUNT = 0


# Lane type, time last visited, car, can change
s = (MILES, LANES, 4)
freeway = np.zeros(s, dtype = object)

#The freeway is represented as a 2D array
def initializeRoad():
	global TOL_COUNT
	global freeway
	global REG_COUNT

	freeway[:, :, 2] = None # initilaize all cars to none
	freeway[:, 1:3, 0] = REGULAR
	freeway[:, 3, 0] = TOLL
	freeway[:, 0, 0] = NOT_USED
	freeway[:, :, 3] = CAN_CHANGE_LANES
	freeway[1232:, 3, 3] = CANNOT_CHANGE_LANES

	for i in range(freeway.shape[0]):  # placing vehicles on the map\
		for j in range(freeway.shape[1]):
			val = np.random.uniform(0, 1)
			if ((j == 1 or j == 2) and val < .5): # placing vehicles on regular lanes
				freeway[i][j][2] = car_agent.Car(i, j, False)  # JUST A STING FOR NOW SINCE TRAN HASN'T DONE THE CLASS YET AND I DONT WANNA FUCK SHIT UP
				REG_COUNT += 1
			elif (j == 3 and val < .25): # placing vehicles on toll lanes
				freeway[i][j][2] = car_agent.Car(i, j, False)
				TOL_COUNT += 1


# Adds the on and off ramps to the freeway
def AddingRampsToFreeway():
	for i in range(len(freeway)):
		#setting the off ramps value to the freeway
		if (i >= 774 and i <= 844) or (i >= 1547 and i <= 1653) or (i >= 1794 and i <= 1900):
			freeway[i, 0, 0] = OFF_RAMP
		 #setting the on ramps value to the freeway
		if (i >= 845 and i <= 951) or (i >= 1654 and i <= 1724) or (i >= 1901 and i <= 2042) or (i >= 2213 and i <= 2320):
			freeway[i, 0, 0] = ON_RAMP

def moveCarsHelper():
	for i in range(freeway.shape[0] - 1, -1, -1):
		for j in range(freeway.shape[1] - 1, -1, -1):
			if type(freeway[i, j, 2]) is car_agent.Car:
				freeway[i, j, 2].drive(freeway, TIME_SECONDS)

def addAgent():
	global REG_COUNT
	global TOL_COUNT
	global TIME_SECONDS
	

	for i in range(1, freeway.shape[1]):
		val = np.random.uniform(0, 1)
		if ((i == 1 or i == 2) and val < .5 and freeway[0, i, 1] != TIME_SECONDS):
			freeway[0][i][2] = car_agent.Car(0, i, False)
			REG_COUNT += 1
		elif (i == 3 and val < .2 and freeway[0, i, 1] != TIME_SECONDS):
			freeway[0, i, 2] = car_agent.Car(0, i, False)
			TOL_COUNT += 1

def moveCars():
	global TIME_SECONDS

	while TIME_SECONDS < 20:
		moveCarsHelper()
		TIME_SECONDS += 1

#Needs more work
def finishLine():
	for i in range(freeway.shape[0]):  # placing vehicles on the map\
		for j in range(freeway.shape[1]):
			car = freeway[i, j, 2]
			#print car.is_tracked()
			pass
				

def visualize():
	visualization = np.zeros([freeway.shape[0], freeway.shape[1]])
	for i in range(freeway.shape[0]):
		for j in range(freeway.shape[1]):
			if freeway[i][j][0] == -1:
				visualization[i][j] = 800
			if freeway[i][j][0] == 1:
				visualization[i][j] = 300
			if freeway[i][j][0] == 3:
				visualization[i][j] = 600
			if freeway[i][j][0] == 2:
				visualization[i][j] = 900
			#if freeway[i][j][2] == None:
			#	visualization[i][j] = 900
			#if type(freeway[i][j][2]) is car_agent.Car:
			#	visualization[i][j] = 1200
			#if freeway[i][j][3] == True:
			#	visualization[i][j] = 1500
			#if freeway[i][j][3] == False:
			#	visualization[i][j] = 1800
			#visualization[i][j] = freeway[i][j][1] * 10

	d = plt.pcolor(visualization, cmap = "gist_ncar")

initializeRoad()
AddingRampsToFreeway()
#finishLine()

freeway[0, 1, 2] = car_agent.Car(0, 1, False)
moveCars()
visualize()
print(REG_COUNT)
print(TOL_COUNT)
plt.show()

top = tkinter.Tk()
top.config(width=400, height=700)
C = tkinter.Canvas(top,bg="dark green", height=700, width=400)
C.create_rectangle(50, 0, 350, 700, fill="grey", outline = 'blue')
C.create_line(125,0,125,700)
C.create_line(200,0,200,700)
C.create_line(273,0,273,700)
C.create_line(277,200,277,700)

#C.pack()
#top.mainloop()



#top = tkinter.Tk()
#top.mainloop()

#print(freeway)
