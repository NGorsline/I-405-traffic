import numpy as np
import car_agent
np.set_printoptions(threshold=np.inf)
import math
#import tkinter
import matplotlib.pyplot as plt
import matplotlib.colors
import time

global freeway
global TIME_SECONDS
global TOL_COUNT
global REG_COUNT
global percentReg
global percentTol
global percentOnramp
global onrampCount
global redLightSpeed
global entrance1
global entrance2
global entrance3
global entrance4


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
#Keeps track of the time of selected vehicles
list = [] 
TOL_COUNT = 0
REG_COUNT = 0
percentReg = .50
percentTol = .25
percentOnramp = .1
onrampCount = 0
redLightSpeed = 8
entrance1 = 845
entrance2 = 1654
entrance3 = 1901
entrance4 = 2213

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
	freeway[:, :, 3] = CANNOT_CHANGE_LANES
	freeway[:, :, 1] = -3000

	for i in range(freeway.shape[0]):  # placing vehicles on the map\
		for j in range(freeway.shape[1]):
			val = np.random.uniform(0, 1)
			if ((j == 1 or j == 2) and val < percentReg): # placing vehicles on regular lanes
				freeway[i][j][2] = car_agent.Car(i, j, False) 
				REG_COUNT += 1
			elif (j == 3 and val < percentTol): # placing vehicles on toll lanes
				freeway[i][j][2] = car_agent.Car(i, j, False)
				TOL_COUNT += 1


# Adds the on and off ramps to the freeway
def AddingRampsToFreeway():
	for i in range(len(freeway)):
		val = np.random.uniform(0, 1)
		#setting the off ramps value to the freeway
		if (i >= 774 and i <= 844) or (i >= 1547 and i <= 1653) or (i >= 1794 and i <= 1900):
			freeway[i, 0, 0] = OFF_RAMP
			if (val < percentOnramp):
				freeway[i, 0, 2] = car_agent.Car(i, 0, False)
		 #setting the on ramps value to the freeway
		if (i >= entrance1 and i <= 951) or (i >= entrance2 and i <= 1724) or (i >= entrance3 and i <= 2042) or (i >= entrance4 and i <= 2320):
			freeway[i, 0, 0] = ON_RAMP
			if (val < percentOnramp):
				freeway[i, 0, 2] = car_agent.Car(i, 0, False)
		 #setting the dotted lines on the toll lane 
		if (i >= 0 and i <=106) or (i >= 489 and i<=630) or (i>=1054 and i<=1265):
				freeway[i, 3, 3] = CAN_CHANGE_LANES

def moveCarsHelper():
	for i in range(freeway.shape[0] - 1, -1, -1):
		for j in range(freeway.shape[1] - 1, -1, -1):
			if type(freeway[i, j, 2]) is car_agent.Car:
				freeway[i, j, 2].drive(freeway, TIME_SECONDS)


def addAgent():
	global REG_COUNT
	global TOL_COUNT
	global TIME_SECONDS
	global redLightSpeed
	global entrance1
	global entrance2
	global entrance3
	global entrance4
	
	for i in range(freeway.shape[1]):
		val = np.random.uniform(0, 1)
		if ((i == 1 or i == 2) and val < percentReg and freeway[0, i, 1] != TIME_SECONDS):
			freeway[0][i][2] = car_agent.Car(0, i, False)
			REG_COUNT += 1
		elif (i == 3 and val < percentTol and freeway[0, i, 1] != TIME_SECONDS):
			freeway[0, i, 2] = car_agent.Car(0, i, False)
			TOL_COUNT += 1

	# adding cars to the on ramps
	if (TIME_SECONDS % redLightSpeed == 0):
		freeway[entrance1][0][2] = car_agent.Car(entrance1, 0, False)
		freeway[entrance2][0][2] = car_agent.Car(entrance2, 0, False)
		freeway[entrance3][0][2] = car_agent.Car(entrance3, 0, False)
		freeway[entrance4][0][2] = car_agent.Car(entrance4, 0, False)

def moveCars():
	global TIME_SECONDS
	i = 0
	if (i == 1):
		freeway[1][1][1] = 90

	while TIME_SECONDS < 200:
		finishLine()
		moveCarsHelper()
		addAgent()
		TIME_SECONDS += 1
		visualize()
		plt.pause(.0001)

#Needs more work
def finishLine():
	global TOL_COUNT
	global REG_COUNT

	i = 6
	#The 6th element before the finish line (element = 2313)
	element = 2313
		#Check for vehicles in the current row
	for j in range(element, freeway.shape[0]):
		for k in range(freeway.shape[1]):
			#if there is a vehicle set it to a variable
			if(freeway[j, k, 2] != None):
				car = freeway[j, k, 2]
				#if the speed is greater than the length that it can travel in one time step
				#calculate the time and store it in a list 
				if ((car.MAX_SPEED) > i):
					if(car.is_tracked()): 
						#Calculating the total time, needs work
						vehicle_total_time = car.MAX_SPEED
						freeway[j, k, 2] = None
						if (k == 3):
							TOL_COUNT -= 1
						else:
							REG_COUNT -= 1
					else:
						freeway[j, k, 2] = None
						if (k == 3):
							TOL_COUNT -= 1
						else:
							REG_COUNT -= 1
		i = i-1		
			
				
######################################################################
# Very Basic Visualization!!!
# 
# Uncomment laneVis parts to see the lanes, uncomment carVis
# parts to see the cars.
#
# Green = Car
# Grey = Road
######################################################################
def visualize():
	laneVis = np.zeros([freeway.shape[0], freeway.shape[1]])
	carVis = np.zeros([100, 4])
	for i in range(100):
		for j in range(4):
			#if freeway[i][j][0] == -1:
			#	laneVis[i][j] = 800
			#if freeway[i][j][0] == 1:
			#	laneVis[i][j] = 300
			#if freeway[i][j][0] == 3:
			#	laneVis[i][j] = 600
			#if freeway[i][j][0] == 2:
			#	laneVis[i][j] = 900
			#if freeway[i][j][0] == 4:
			#	laneVis[i][j] = 100
			if freeway[i + 0][j][2] == None:
				carVis[i][j] = 900
			if type(freeway[i + 0][j][2]) is car_agent.Car:
				carVis[i][j] = 100

	
	#d = plt.pcolor(laneVis, cmap = "gist_ncar")
	c = plt.pcolor(carVis, cmap = "Dark2")




###################################################################################
######## created a smaller freeway of size 20 by 4 for testing purposes###########
###################################################################################
global small_freeway
a = (20, 4, 4)
small_freeway = np.zeros(a, dtype = object)
def test_freeway():
	global small_freeway
	small_freeway[:, :, 2] = None # initilaize all cars to none
	small_freeway[:, 1:3, 0] = REGULAR
	small_freeway[:, 3, 0] = TOLL
	small_freeway[:, 0, 0] = NOT_USED
	small_freeway[:, :, 3] = CAN_CHANGE_LANES

	for i in range(small_freeway.shape[0]):  # placing vehicles on the map\
		for j in range(small_freeway.shape[1]):
			val = np.random.uniform(0, 1)
			if ((j == 1 or j == 2) and val < .5): # placing vehicles on regular lanes
				small_freeway[i][j][2] = car_agent.Car(i, j, False)  # JUST A STING FOR NOW SINCE TRAN HASN'T DONE THE CLASS YET AND I DONT WANNA FUCK SHIT UP
			elif (j == 3 and val < .25): # placing vehicles on toll lanes
				small_freeway[i][j][2] = car_agent.Car(i, j, False)


#################
#Calling Methods# 
#################
initializeRoad()
AddingRampsToFreeway()
#finishLine()
freeway[0, 1, 2] = car_agent.Car(0, 1, False)
freeway[1, 2, 2] = car_agent.Car(1, 2, False)
freeway[2, 1, 2] = car_agent.Car(2, 1, False)
freeway[3, 1, 2] = car_agent.Car(3, 1, False)
freeway[4, 1, 2] = car_agent.Car(4, 1, False)

moveCars()
#test_freeway()
print("Cars on regular lanes: ", REG_COUNT)
print("Cars on toll lanes: ", TOL_COUNT)
#####################################################################
#####################################################################


#top = tkinter.Tk()
#top.config(width=400, height=700)
#C = tkinter.Canvas(top,bg="dark green", height=700, width=400)
#C.create_rectangle(50, 0, 350, 700, fill="grey", outline = 'blue')
#C.create_line(125,0,125,700)
#C.create_line(200,0,200,700)
#C.create_line(273,0,273,700)
#C.create_line(277,200,277,700)

#C.pack()
#top.mainloop()



#top = tkinter.Tk()
#top.mainloop()

#print(freeway)
