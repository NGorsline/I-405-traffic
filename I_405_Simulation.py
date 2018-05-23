import numpy as np
import car_agent
np.set_printoptions(threshold=np.inf)
import math
import tkinter

import time

global freeway

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


# Lane type, time last visited, car, can change
s = (MILES, LANES, 4)
freeway = np.zeros(s, dtype = object)

#The freeway is represented as a 2D array
def initializeRoad():
	global freeway
	freeway[:, :, 2] = None # initilaize all cars to none
	freeway[:, 1:3, 0] = REGULAR
	freeway[:, 3, 0] = TOLL
	freeway[:, 0, 0] = NOT_USED
	freeway[:, :, 3] = CAN_CHANGE_LANES
	freeway[1232:, 3, 3] = CANNOT_CHANGE_LANES

	for i in range(freeway.shape[0]):  # placing vehicles on the map
		for j in range(freeway.shape[1]):
			val = np.random.uniform(0, 1)
			if ((j == 1 or j == 2) and val < .5): # placing vehicles on regular lanes
				freeway[i][j][2] = car_agent.Car(i, j)  # JUST A STING FOR NOW SINCE TRAN HASN'T DONE THE CLASS YET AND I DONT WANNA FUCK SHIT UP
			elif (j == 3 and val < .25): # placing vehicles on toll lanes
				freeway[i][j][2] = car_agent.Car(i, j)

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
				freeway[i, j, 2].drive(freeway)

def moveCars():
	time = 0
	while time < 2000:
		moveCarsHelper()
		time += 1

initializeRoad()
AddingRampsToFreeway()
freeway[0, 1, 2] = car_agent.Car(0, 1)

moveCars()

top = tkinter.Tk()
top.mainloop()

#print(freeway)
