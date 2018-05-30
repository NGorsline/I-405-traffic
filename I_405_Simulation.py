import numpy as np
import car_agent
np.set_printoptions(threshold=np.inf)
import math
#import tkinter
import matplotlib.pyplot as plt
import matplotlib.colors
import time
import random

global freeway
global TIME_SECONDS
global TOL_COUNT
global REG_COUNT
global percentReg
global percentTol
global percentOnramp
global onrampCount
global redLightSpeed
global trackedSpeed
global trackedCount
global tollTrackedCount
global entrance1
global entrance2
global entrance3
global entrance4
global numAttributes
global starterTimeVal
global timeStepList
global numLanes
global numTollLanes


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
tollList = []
TOL_COUNT = 0
REG_COUNT = 0
percentReg = .5
percentTol = .25
percentOnramp = .1
onrampCount = 0
redLightSpeed = 8
entrance1 = 845
entrance2 = 1654
entrance3 = 1901
entrance4 = 2213
trackedSpeed = 30 # every 30 seconds we add a new tracked agent
trackedCount = 0
tollTrackedCount = 0
numLanes = 4
starterTimeVal = -3000
numAttributes = 4
timeStepList = []
numLanes = 2
numTollLanes = 1

#controls how many spaces before and after the off and on 
#ramps are available for cars to move in and out
OFF_RAMP_SPACES = 10
ON_RAMP_SPACES = 10


#The freeway is represented as a 2D array
def initializeRoad():
	global TOL_COUNT
	global freeway
	global REG_COUNT
	global TIME_SECONDS
	global starterTimeVal
	global MILES
	global LANES
	global numLanes
	global timeStepList

	# Lane type, time last visited, car, can change
	s = (MILES, LANES, numAttributes)
	freeway = np.zeros(s, dtype = object)

	freeway[:, :, 2] = None # initilaize all cars to none
	freeway[:, 1:3, 0] = REGULAR
	freeway[:, 3, 0] = TOLL
	freeway[:, 0, 0] = NOT_USED
	freeway[:, :, 3] = CANNOT_CHANGE_LANES
	freeway[:, :, 1] = starterTimeVal

	"""If cars are not initialized all added vehicles will make it to the end of the freeway in 6.5 minutes"""

	for i in range(freeway.shape[0]):  # placing vehicles on the map\
		for j in range(freeway.shape[1]):
			val = np.random.uniform(0, 1)
			if ((j == 1 or j == 2) and val < percentReg): # placing vehicles on regular lanes
				freeway[i][j][2] = car_agent.Car(i, j, False, TIME_SECONDS) 
				REG_COUNT += 1
			elif (j == 3 and val < percentTol): # placing vehicles on toll lanes
				freeway[i][j][2] = car_agent.Car(i, j, False, TIME_SECONDS)
				TOL_COUNT += 1

	t = (REG_COUNT, TOL_COUNT)
	timeStepList.append(t)

	AddingRampsToFreeway()

def initializeEmpty():
	global freeway
	global starterTimeVal
	global MILES
	global LANES
	global numLanes

	# Lane type, time last visited, car, can change
	s = (MILES, LANES, numLanes)
	freeway = np.zeros(s, dtype = object)

	freeway[:, :, 2] = None # initilaize all cars to none
	freeway[:, 1:3, 0] = REGULAR
	freeway[:, 3, 0] = TOLL
	freeway[:, 0, 0] = NOT_USED
	freeway[:, :, 3] = CANNOT_CHANGE_LANES
	freeway[:, :, 1] = starterTimeVal

def initializeExtraTollLane():
	global TOL_COUNT
	global freeway
	global REG_COUNT
	global TIME_SECONDS
	global starterTimeVal
	global MILES
	global LANES
	global numAttributes
	global timeStepList
	global numLanes
	global numTollLanes
	LANES = 5

	numLanes = 2
	numTollLanes = 2
	s = (MILES, LANES, numAttributes)
	freeway = np.zeros(s, dtype = object)

	freeway[:, :, 2] = None			# initilaize all cars to none
	freeway[:, 1:3, 0] = REGULAR
	freeway[:, 3:5, 0] = TOLL
	freeway[:, 0, 0] = NOT_USED
	freeway[:, :, 3] = CANNOT_CHANGE_LANES
	freeway[:, :, 1] = starterTimeVal

	# getting number of regular cars that were initialized in the control simulation
	regCount = timeStepList[0][0]
	# getting number of toll cars
	tollCount = timeStepList[0][1]

	# we pick a random spot on the freeway to initialize a car, and set it to a car
	while regCount > 0:
		x = random.randint(1, 2)
		y = random.randint(0, freeway.shape[0] - 1)

		# check if the spot is occupied
		if (freeway[y, x, 2] == None):
			freeway[y, x, 2] = car_agent.Car(y, x, False, TIME_SECONDS)
			regCount -= 1

		# Here we initialize the toll lane
	while tollCount > 0:
		x = random.randint(3, 4)
		y = random.randint(0, freeway.shape[0] - 1)
		if (freeway[y, x, 2] == None):
			freeway[y, x, 2] = car_agent.Car(y, x, False, TIME_SECONDS)
			tollCount -= 1


	AddingRampsToFreeway()


# Adds the on and off ramps to the freeway
def AddingRampsToFreeway():
	global REG_COUNT

	for i in range(len(freeway)):
		val = np.random.uniform(0, 1)
		#setting the off ramps value to the freeway
		if (i >= 774 and i <= 844) or (i >= 1547 and i <= 1653) or (i >= 1794 and i <= 1900):
			freeway[i, 0, 0] = OFF_RAMP
			if (val < percentOnramp):
				freeway[i, 0, 2] = car_agent.Car(i, 0, False, TIME_SECONDS)
				REG_COUNT += 1
		 #setting the on ramps value to the freeway
		if (i >= entrance1 and i <= 951) or (i >= entrance2 and i <= 1724) or (i >= entrance3 and i <= 2042) or (i >= entrance4 and i <= 2320):
			freeway[i, 0, 0] = ON_RAMP
			if (val < percentOnramp):
				freeway[i, 0, 2] = car_agent.Car(i, 0, False, TIME_SECONDS)
				REG_COUNT += 1
		 #setting the dotted lines on the toll lane 
		if (i >= 0 and i <=106) or (i >= 489 and i<=630) or (i>=1054 and i<=1265):
				freeway[i, 3, 3] = CAN_CHANGE_LANES

#applies the available spaces for cars to move in and out
#before and after the off and on ramps 
def markAvailableSpaces():
	counter = 0
	#flag to stop the exit spaces
	flag = True
	for i in range(len(freeway)-ON_RAMP_SPACES):
		#marks the off_ramp_spaces elements of the exit ramp
		if freeway[i, 0, 0] == 2 and flag == True:
			freeway[i, 0, 3] = True
			counter = counter + 1
			if (counter == OFF_RAMP_SPACES):
				flag = False
				counter = 0
		#marks the on_ramp_spaces elements of the on ramp
		if freeway[i, 0, 0] == 4 and freeway[i+ON_RAMP_SPACES, 0, 0] != 4:
			freeway[i, 1, 3] = True
			if(flag == False):
				flag = True


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
	global tollTrackedCount
	global trackedCount
	global trackedSpeed
	global timeStepList
	regAddCount = 0
	tollAddCount = 0

	for i in range(freeway.shape[1]):
		val = np.random.uniform(0, 1)
		hasSet = False
		if ((i == 1 or i == 2) and val < percentReg and freeway[0, i, 1] != TIME_SECONDS):
			freeway[0][i][2] = car_agent.Car(0, i, False, TIME_SECONDS)
			REG_COUNT += 1
			regAddCount += 1
			if (TIME_SECONDS % trackedSpeed == 0 and trackedCount < 30 and hasSet == False):
				freeway[0][i][2].tracked = True
				trackedCount += 1
				hasSet = True
		elif (i == 3 and val < percentTol and freeway[0, i, 1] != TIME_SECONDS):
			freeway[0, i, 2] = car_agent.Car(0, i, False, TIME_SECONDS)
			TOL_COUNT += 1
			tollAddCount += 1
			if (TIME_SECONDS % trackedSpeed == 0 and trackedCount < 30 and hasSet == False):
				freeway[0][i][2].tracked = True
				tollTrackedCount += 1
				hasSet = True
	t = (regAddCount, tollAddCount)
	timeStepList.append(t) # take timeseconds out of tuple
	regAddCount = 0
	tollAddCount = 0

	# adding cars to the on ramps
	if (TIME_SECONDS % redLightSpeed == 0):

		# each entrance is a different entrance point on the freeway. All the stoplights are synced up in this simulation
		freeway[entrance1][0][2] = car_agent.Car(entrance1, 0, False, TIME_SECONDS)
		freeway[entrance2][0][2] = car_agent.Car(entrance2, 0, False, TIME_SECONDS)
		freeway[entrance3][0][2] = car_agent.Car(entrance3, 0, False, TIME_SECONDS)
		freeway[entrance4][0][2] = car_agent.Car(entrance4, 0, False, TIME_SECONDS)
		REG_COUNT += 4

def addAgentNewLayout():
	global REG_COUNT
	global TOL_COUNT
	global TIME_SECONDS
	global redLightSpeed
	global entrance1
	global entrance2
	global entrance3
	global entrance4
	global tollTrackedCount
	global trackedCount
	global trackedSpeed
	global timeStepList
	global numLanes
	global numTollLanes
	backup = 0
	tollBackup = 0
	laneStart = -1
	tollStart = -1

	# finding when the lanes/toll lanes start
	for i in range(freeway.shape[1]):
		if freeway[0, i, 0] == 1 and laneStart == -1:
			laneStart = i
		elif freeway[0, i, 0] == 3 and tollStart == -1:
			tollStart = i
	
	# if there are more cars to be added then there are lanes
	if timeStepList[TIME_SECONDS + 1][0] > numLanes:
		backup = timeStepList[TIME_SECONDS][0] - numLanes
		for j in range(freeway.shape[1]):
			if freeway[0, j, 0] == 1:
				freeway[0, j, 2] = car_agent.Car(0, j, False, TIME_SECONDS)
	else:
		hasSet = False
		carsToAdd = timeStepList[TIME_SECONDS + 1][0]
		loopCount = 0
		loopCountMax = numLanes * 10 # if loop count Max is reached TIME_SECONDS must be off
		while carsToAdd > 0 and loopCount != loopCountMax:
			x = random.randint(laneStart, laneStart + numLanes - 1)
			if freeway[0, x, 2] == None and freeway[0, x, 1] != TIME_SECONDS:
				freeway[0, x, 2] = car_agent.Car(0, x, False, TIME_SECONDS)
				carsToAdd -= 1
				loopCount += 1
				if (TIME_SECONDS % trackedSpeed == 0 and hasSet == False):
					freeway[0][x][2].tracked = True
					trackedCount += 1
					hasSet = True
		backup += carsToAdd

		# adding backed up cars into the simulation
		if backup > 0:
			for j in range(laneStart, laneStart + numLanes):
				if backup > 0:
					if freeway[0, j, 2] == None and freeway[0, x, 1] != TIME_SECONDS:
						freeway[0, j, 2] = car_agent.Car(0, j, False, TIME_SECONDS)
						backup -= 1

		# adding cars to the toll lanes
		tollCarsToAdd = timeStepList[TIME_SECONDS + 1][1]
		loopCount = 0
		loopCountMax = numTollLanes * 10 # if loop count Max is reached TIME_SECONDS must be off
		while tollCarsToAdd > 0 and loopCount != loopCountMax:
			x = random.randint(tollStart, tollStart + numTollLanes - 1)
			if freeway[0, x, 2] == None and freeway[0, x, 1] != TIME_SECONDS:
				freeway[0, x, 2] = car_agent.Car(0, x, False, TIME_SECONDS)
				tollCarsToAdd -= 1
				loopCount += 1
				if (TIME_SECONDS % trackedSpeed == 0 and hasSet == False):
					freeway[0][x][2].tracked = True
					tollTrackedCount += 1
					hasSet = True
		tollBackup += tollCarsToAdd

		# adding backed up toll cars into the simulation
		if tollBackup > 0:
			for j in range(freeway.shape[1]):
				if tollBackup > 0:
					if freeway[0, j, 2] == None and freeway[0, x, 1] != TIME_SECONDS:
						freeway[0, j, 2] = car_agent.Car(0, j, False, TIME_SECONDS)
						tollBackup -= 1

	
	# adding cars to the on ramps
	if (TIME_SECONDS % redLightSpeed == 0):

		# each entrance is a different entrance point on the freeway. All the stoplights are synced up in this simulation
		freeway[entrance1][0][2] = car_agent.Car(entrance1, 0, False, TIME_SECONDS)
		freeway[entrance2][0][2] = car_agent.Car(entrance2, 0, False, TIME_SECONDS)
		freeway[entrance3][0][2] = car_agent.Car(entrance3, 0, False, TIME_SECONDS)
		freeway[entrance4][0][2] = car_agent.Car(entrance4, 0, False, TIME_SECONDS)
		REG_COUNT += 4

def moveCars():
	global TIME_SECONDS
	global trackedCount
	while len(list) != 30:
		finishLine()
		moveCarsHelper()
		addAgent()
		TIME_SECONDS += 1
		#plt.figure(1)
		#visualize()
		#plt.pause(.0001)
		#plt.figure(2)
		#congestionVis()
		#plt.pause(.0001)


#Needs more work
def finishLine():
	global TOL_COUNT
	global REG_COUNT
	global tollTrackedCount
	global trackedCount

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
						vehicle_total_time = TIME_SECONDS - car.start_time()
						freeway[j, k, 2] = None
						if (k == 3):
							tollTrackedCount -= 1
							tollList.append(vehicle_total_time)
						else:
							list.append(vehicle_total_time)
							trackedCount -= 1
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
	global numAttributes

	laneVis = np.zeros([freeway.shape[0], freeway.shape[1]])
	carVis = np.zeros([2320, freeway.shape[1]])
	for i in range(2320):
		for j in range(freeway.shape[1]):
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
				if freeway[i + 0, j, 2].is_tracked():
					carVis[i][j] = 400

	#d = plt.pcolor(laneVis, cmap = "gist_ncar")
	c = plt.pcolor(carVis, cmap = "Dark2")

def congestionVis():
	visList = []
	carCount = 0

	for i in range(0, freeway.shape[0], 580):
		for j in range(i, i + 580):
			for k in range(4):
				if type(freeway[j, k, 2]) is car_agent.Car and k != 0: 
					carCount += 1
		t = (carCount, carCount)
		visList.append(t)
		carCount = 0

	c = plt.pcolor(visList, cmap = "rainbow")

def moveCarsChanged():
	global TIME_SECONDS
	global trackedCount
	global timeStepList
	while TIME_SECONDS + 1 < len(timeStepList):
		finishLine()
		moveCarsHelper()
		addAgentNewLayout()
		TIME_SECONDS += 1
		#plt.figure(1)
		#visualize()
		#plt.pause(.0001)

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
				small_freeway[i][j][2] = car_agent.Car(i, j, False, TIME_SECONDS)  # JUST A STING FOR NOW SINCE TRAN HASN'T DONE THE CLASS YET AND I DONT WANNA FUCK SHIT UP
			elif (j == 3 and val < .25): # placing vehicles on toll lanes
				small_freeway[i][j][2] = car_agent.Car(i, j, False, TIME_SECONDS)

def displayOutput():
	print("Cars on regular lanes: ", REG_COUNT)
	print("Cars on toll lanes: ", TOL_COUNT)

	for i in range(len(list)):
		print("Agent", i + 1, ": ", round(list[i] / 60, 2), " minutes")

	print()
	print("*********************************************************************************************")
	print("*********************************************************************************************")
	print()

	for i in range(len(tollList)):
		print("Toll Agent", i + 1, ": ", round(tollList[i] / 60, 2), " minutes")

	print()
	print("*********************************************************************************************")
	print("*********************************************************************************************")
	print()

	array = np.array(list)
	tolArray = np.array(tollList)

	print ("Average time for a regular car to finish simulation: ", round(array.mean() / 60, 2), " minutes")
	print ("Average time for a tol lane car to finish simulation: ", round(tolArray.mean() / 60, 2), " minutes") 

#################
#Calling Methods# 
#################

# Initializes the basic road. 
initializeRoad()


# No cars initialized beforehand. Cars only enter from the start of the freeway
#initializeEmpty()

print("moveCars")
moveCars()
displayOutput()
TIME_SECONDS = 0
trackedCount = 0
list = []

print("extra toll lane")
# Adding one extra toll lane
initializeExtraTollLane()
print("moving cars")
moveCarsChanged()
displayOutput()


#test_freeway()
#######################################################
#######################################################



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
