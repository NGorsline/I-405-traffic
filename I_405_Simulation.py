import numpy as np
import car_agent
np.set_printoptions(threshold=np.inf)
import math
import matplotlib.pyplot as plt
import matplotlib.colors
import time
import random

#global variables
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
global onramp1B
global onramp2B
global onramp3B
global offramp4B
global numAttributes
global starterTimeVal
global timeStepList
global numLanes
global numTollLanes
global onramp1
global onramp2
global onramp3
global onramp4
global addedYet
global speed
global onrampSpeed
global cutoff
global totalCarCount
global time
global toll

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

#list of total time for vehicles on the toll lane
tollList = []
TOL_COUNT = 0
REG_COUNT = 0
percentReg = .99
percentTol = .05
percentOnramp = .9
onrampCount = 0
redLightSpeed = 5
cutoff = 15
totalCarCount = 0
time = 4.5
toll = 1.7

# Off ramps begins  
offramp1B = 774
offramp2B = 1547
offramp3B = 1794
offramp4B = 2214
# Off ramps ends 
offramp1E = 844
offramp2E = 1653
offramp3E = 1900
offramp4E = 2319
# On ramps begins
onramp1B = 845
onramp2B = 1654
onramp3B = 1901
# On ramps ends
onramp1E = 951
onramp2E = 1724
onramp3E = 2042

# Off ramps onramp  
offramp1 = 774
offramp2 = 1547
offramp3 = 1794
# On ramps onramp
onramp1 = 845
onramp2 = 1654
onramp3 = 1901
onramp4 = 2213

# every 30 seconds we add a new tracked agent
trackedSpeed = 30 
trackedCount = 0
tollTrackedCount = 0
numLanes = 4
starterTimeVal = -3000
numAttributes = 4
timeStepList = []
numLanes = 2
numTollLanes = 1
speed = 6
onrampSpeed = 0

#The available spaces for cars to move in and out
#in the off and on ramps 
OFF_RAMP_SPACES = 10
ON_RAMP_SPACES = 10

#removes vehicles after entering to the exit lane after so many feet 
REMOVE_VEHICLE = 6

#On ramps Constants for the moveFreewayOnRamp(onRamp,direction,indexes) method
ON_RAMP_ONE = onramp1B
ON_RAMP_TWO = onramp2B
ON_RAMP_THREE = onramp3B

# Lane type, time last visited, car, can change
s = (MILES, LANES, 4)
freeway = np.zeros(s, dtype = object)

#The freeway is represented as a 2D array
def initializeRoad():
	global TOL_COUNT
	global freeway
	global time
	global toll
	global REG_COUNT
	global TIME_SECONDS
	global starterTimeVal
	global MILES
	global LANES
	global numLanes
	global timeStepList
	global speed

	# Lane type, time last visited, car, can change
	s = (MILES, LANES, numAttributes)
	freeway = np.zeros(s, dtype = object)
	#time = 5.5
	#toll = 1.2
	#time = 
	#toll = 1

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
			speed = random.randint(0, 1)
			if ((j == 1 or j == 2) and val < percentReg): # placing vehicles on regular lanes
				freeway[i][j][2] = car_agent.Car(i, j, False, TIME_SECONDS, speed) 
				REG_COUNT += 1
			elif (j == 3 and val < percentTol): # placing vehicles on toll lanes
				freeway[i][j][2] = car_agent.Car(i, j, False, TIME_SECONDS, speed)
				TOL_COUNT += 1

	t = (REG_COUNT, TOL_COUNT)
	timeStepList.append(t)
	AddingRampsToFreeway()
	markAvailableSpaces()

def initializeEmpty():
	global freeway
	global starterTimeVal
	global MILES
	global LANES
	global numLanes
	global time
	global toll

	# Lane type, time last visited, car, can change
	s = (MILES, LANES, numAttributes)
	freeway = np.zeros(s, dtype = object)

	time = 1
	toll = 1
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
	global time
	global toll
	global numAttributes
	global timeStepList
	global numLanes
	global numTollLanes
	LANES = 5

	toll = 1
	time = 4.5
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
			speed = random.randint(0, 1)
			freeway[y, x, 2] = car_agent.Car(y, x, False, TIME_SECONDS, speed)
			regCount -= 1

		# Here we initialize the toll lane
	while tollCount > 0:
		x = random.randint(3, 4)
		y = random.randint(0, freeway.shape[0] - 1)
		if (freeway[y, x, 2] == None):
			speed = random.randint(0, 1)
			freeway[y, x, 2] = car_agent.Car(y, x, False, TIME_SECONDS, speed)
			tollCount -= 1


	AddingRampsToFreeway()
	markAvailableSpaces()

def makeTollRegular():
	global TOL_COUNT
	global freeway
	global REG_COUNT
	global TIME_SECONDS
	global starterTimeVal
	global time
	global toll
	global MILES
	global LANES
	global numLanes
	global timeStepList
	numLanes = 3
	numTollLanes = 0
	time = 3.9

	# Lane type, time last visited, car, can change
	s = (MILES, LANES, numAttributes)
	freeway = np.zeros(s, dtype = object)

	freeway[:, :, 2] = None # initilaize all cars to none
	freeway[:, 1:4, 0] = REGULAR
	freeway[:, 0, 0] = NOT_USED
	freeway[:, :, 3] = CANNOT_CHANGE_LANES
	freeway[:, :, 1] = starterTimeVal

	"""If cars are not initialized all added vehicles will make it to the end of the freeway in 6.5 minutes"""

	# getting number of regular cars that were initialized in the control simulation
	regCount = timeStepList[0][0]
	# getting number of toll cars
	tollCount = timeStepList[0][1]
	regCount += tollCount

	# we pick a random spot on the freeway to initialize a car, and set it to a car
	while regCount > 0:
		x = random.randint(1, 3)
		y = random.randint(0, freeway.shape[0] - 1)

		# check if the spot is occupied
		if (freeway[y, x, 2] == None):
			speed = random.randint(0, 1)
			freeway[y, x, 2] = car_agent.Car(y, x, False, TIME_SECONDS, speed)
			regCount -= 1

	AddingRampsToFreeway()
	markAvailableSpaces()

# Adds the on and off ramps to the freeway

def initializeExtraLane():
	global TOL_COUNT
	global freeway
	global REG_COUNT
	global TIME_SECONDS
	global starterTimeVal
	global time
	global toll
	global MILES
	global LANES
	global numLanes
	global timeStepList
	numLanes = 3
	numTollLanes = 1
	time = 3.6
	#toll = 1.2
	LANES = 5

	# Lane type, time last visited, car, can change
	s = (MILES, LANES, numAttributes)
	freeway = np.zeros(s, dtype = object)

	freeway[:, :, 2] = None # initilaize all cars to none
	freeway[:, 1:4, 0] = REGULAR
	freeway[:, 4, 0] = TOLL
	freeway[:, 0, 0] = NOT_USED
	freeway[:, :, 3] = CANNOT_CHANGE_LANES
	freeway[:, :, 1] = starterTimeVal

	"""If cars are not initialized all added vehicles will make it to the end of the freeway in 6.5 minutes"""

	# getting number of regular cars that were initialized in the control simulation
	regCount = timeStepList[0][0]
	# getting number of toll cars
	tollCount = timeStepList[0][1]

	# we pick a random spot on the freeway to initialize a car, and set it to a car
	while regCount > 0:
		x = random.randint(1, 3)
		y = random.randint(0, freeway.shape[0] - 1)

		# check if the spot is occupied
		if (freeway[y, x, 2] == None):
			freeway[y, x, 2] = car_agent.Car(y, x, False, TIME_SECONDS, speed)
			regCount -= 1

		# Here we initialize the toll lane
	while tollCount > 0:
		x = random.randint(4, 4)
		y = random.randint(0, freeway.shape[0] - 1)
		if (freeway[y, x, 2] == None):
			freeway[y, x, 2] = car_agent.Car(y, x, False, TIME_SECONDS, speed)
			tollCount -= 1

	AddingRampsToFreeway()
	markAvailableSpaces()

def AddingRampsToFreeway():
	global REG_COUNT

	for i in range(len(freeway)):
		val = np.random.uniform(0, 1)
		#setting the off ramps values to the freeway
		if (i >= offramp1B and i <= offramp1E) or (i >= offramp2B and i <= offramp2E) or (i >= offramp3B and i <= offramp3E) or (i >= offramp4B and i <= offramp4E):
			freeway[i, 0, 0] = OFF_RAMP
		 #setting the on ramps values to the freeway
		if (i >= onramp1B and i <= onramp1E) or (i >= onramp2B and i <= onramp2E) or (i >= onramp3B and i <= onramp3E):
			freeway[i, 0, 0] = ON_RAMP
			if (val < percentOnramp):
				freeway[i, 0, 2] = car_agent.Car(i, 0, False, TIME_SECONDS, speed)
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

#Removes vehicles of the map once they enter the off-ramp
def removeVehicleFromExitLane():
		flag = True
		for i in range(len(freeway)-REMOVE_VEHICLE):
			if freeway[i, 0, 0] == OFF_RAMP and flag == True:
				#Remove vehicles from the exit lane
				for j in range(REMOVE_VEHICLE):
					freeway[j+i, 0, 2] = None
				flag = False
			if freeway[i,0,0] == ON_RAMP:
				flag = True

def moveCarsHelper():
	global totalCarCount
	totalCarCount = 0

	for i in range(freeway.shape[0] - 1, -1, -1):
		for j in range(freeway.shape[1] - 1, -1, -1):
			if type(freeway[i, j, 2]) is car_agent.Car:
				totalCarCount += 1
				freeway[i, j, 2].drive(freeway, TIME_SECONDS)


def addAgent():
	global REG_COUNT
	global TOL_COUNT
	global TIME_SECONDS
	global redLightSpeed
	global onramp1B
	global onramp2B
	global onramp3B
	global offramp4B
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
			freeway[0][i][2] = car_agent.Car(0, i, False, TIME_SECONDS, speed)
			REG_COUNT += 1
			regAddCount += 1
			if (TIME_SECONDS % trackedSpeed == 0 and trackedCount < 30 and hasSet == False):
				freeway[0][i][2].tracked = True
				trackedCount += 1
				hasSet = True
		elif (i == 3 and val < percentTol and freeway[0, i, 1] != TIME_SECONDS):
			freeway[0, i, 2] = car_agent.Car(0, i, False, TIME_SECONDS, speed)
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

		# each onramp is a different onramp point on the freeway. All the stoplights are synced up in this simulation
		freeway[onramp1][0][2] = car_agent.Car(onramp1, 0, False, TIME_SECONDS, onrampSpeed)
		freeway[onramp2][0][2] = car_agent.Car(onramp2, 0, False, TIME_SECONDS, onrampSpeed)
		freeway[onramp3][0][2] = car_agent.Car(onramp3, 0, False, TIME_SECONDS, onrampSpeed)
		REG_COUNT += 3

def addAgentNewLayout():
	global REG_COUNT
	global TOL_COUNT
	global TIME_SECONDS
	global redLightSpeed
	global onramp1
	global onramp2
	global onramp3
	global onramp4
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
	#print("found when the lanes start")

	if tollStart == -1:
		#print("in no toll lane section")
		hasSet = False
		carsToAdd = timeStepList[TIME_SECONDS + 1][0] + timeStepList[TIME_SECONDS + 1][0]
		loopCount = 0
		loopCountMax = numLanes * 20 # if loop count Max is reached TIME_SECONDS must be off
		while carsToAdd > 0 and loopCount != loopCountMax:
			loopCount += 1
			x = random.randint(laneStart, laneStart + numLanes - 1)
			if freeway[0, x, 2] == None and freeway[0, x, 1] != TIME_SECONDS:
				freeway[0, x, 2] = car_agent.Car(0, x, False, TIME_SECONDS, speed)
				carsToAdd -= 1
				if (TIME_SECONDS % trackedSpeed == 0 and hasSet == False):
					freeway[0][x][2].tracked = True
					trackedCount += 1
					hasSet = True
	else:
	
		# if there are more cars to be added then there are lanes
		if timeStepList[TIME_SECONDS + 1][0] > numLanes:
			backup = timeStepList[TIME_SECONDS][0] - numLanes
			for j in range(freeway.shape[1]):
				if freeway[0, j, 0] == 1:
					freeway[0, j, 2] = car_agent.Car(0, j, False, TIME_SECONDS, speed)
		
		else:
			#print("if too many cars done")
			hasSet = False
			carsToAdd = timeStepList[TIME_SECONDS + 1][0]
			loopCount = 0
			loopCountMax = numLanes * 10 # if loop count Max is reached TIME_SECONDS must be off
			#print("before while loop")
			while carsToAdd > 0 and loopCount != loopCountMax:
				x = random.randint(laneStart, laneStart + numLanes - 1)
				loopCount += 1
				if freeway[0, x, 2] == None and freeway[0, x, 1] != TIME_SECONDS:
					freeway[0, x, 2] = car_agent.Car(0, x, False, TIME_SECONDS, speed)
					carsToAdd -= 1
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
							freeway[0, j, 2] = car_agent.Car(0, j, False, TIME_SECONDS, speed)
							backup -= 1
			
			# adding cars to the toll lanes
			tollCarsToAdd = timeStepList[TIME_SECONDS + 1][1]
			loopCount = 0
			loopCountMax = numTollLanes * 10 # if loop count Max is reached TIME_SECONDS must be off
			while tollCarsToAdd > 0 and loopCount != loopCountMax:
				loopCount += 1
				x = random.randint(tollStart, tollStart + numTollLanes - 1)
				if freeway[0, x, 2] == None and freeway[0, x, 1] != TIME_SECONDS:
					freeway[0, x, 2] = car_agent.Car(0, x, False, TIME_SECONDS, speed)
					tollCarsToAdd -= 1
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
							freeway[0, j, 2] = car_agent.Car(0, j, False, TIME_SECONDS, speed)
							tollBackup -= 1

	# adding cars to the on ramps
	if (TIME_SECONDS % redLightSpeed == 0):
		freeway[onramp1][0][2] = car_agent.Car(onramp1, 0, False, TIME_SECONDS, onrampSpeed)
		freeway[onramp2][0][2] = car_agent.Car(onramp2, 0, False, TIME_SECONDS, onrampSpeed)
		freeway[onramp3][0][2] = car_agent.Car(onramp3, 0, False, TIME_SECONDS, onrampSpeed)
		REG_COUNT += 3


def moveCars():
	global TIME_SECONDS
	global trackedCount
	global totalCarCount

	while len(list) != cutoff:
		removeVehicleFromExitLane()
		finishLine()
		moveCarsHelper()
		addAgent()
		TIME_SECONDS += 1
		plt.axis('off')
		plt.figure(1)
		visualize()
		plt.pause(.001)

#Removes vehicles from the map once they reach the finish line 
def finishLine():
	global TOL_COUNT
	global REG_COUNT
	global tollTrackedCount
	global trackedCount
	global toll
	global time
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
							tollList.append(int(vehicle_total_time) * toll)
						else:
							list.append(vehicle_total_time * time)
							trackedCount -= 1
					else:
						freeway[j, k, 2] = None
						if (k == 3):
							TOL_COUNT -= 1
						else:
							REG_COUNT -= 1
		i = i-1		
			
######################################################################
# Visualization!!!
#
# Green = Car
# Grey = Road
# Pink = Tracked Car
######################################################################
def visualize():
	global numAttributes
	endValue = 2319

	laneVis = np.zeros([freeway.shape[0], freeway.shape[1]])
	carVis = np.zeros([endValue, freeway.shape[1]])
	for i in range(endValue):
		for j in range(freeway.shape[1]):
			if freeway[endValue - (i + 0)][j][2] == None:
				carVis[i][j] = 900
			if type(freeway[endValue - (i + 0)][j][2]) is car_agent.Car:
				carVis[i][j] = 100
				if freeway[endValue - (i + 0), j, 2].is_tracked():
					carVis[i][j] = 400

	c = plt.pcolor(carVis, cmap = "Dark2")


#moves the freeway on-ramp fowards or backwards by specified number of indexes.
#To use this method, pass in the on-ramp variable(ON_RAMP_ONE, ON_RAMP_TWO, ON_RAMP_THREE),
#The direction("F") for moving the on-ramp fowards or ("B") for moving it backwards,
#And the amount of indexes you would like to move the ramp by.
def moveFreewayOnRamp(onRamp,direction,indexes):
	#stores the available backwards spaces for ramp one
	ramp1RearMovement = offramp1B - 1;
	#stores the available spaces for ramp three to move forwards
	ramp1FrontMovement = offramp2B - onramp1E;
	#stores the available backwards spaces for ramp two
	ramp2RearMovement = ramp1FrontMovement -1;
	#stores the available spaces for ramp two to move forwards
	ramp2FrontMovement = offramp3B - onramp2E;
	#stores the available backwards spaces for ramp three
	ramp3RearMovement = ramp2FrontMovement;
	#stores the available spaces for ramp three to move forwards
	ramp3FrontMovement = offramp4B - onramp3E;
	
	# Moves the specified on-ramp forward
	if(direction == 'f' or direction == 'F'):
		#Move on-ramp 1
		if(onRamp == ON_RAMP_ONE):
			if (indexes >= ramp1FrontMovement):
				print ("Can't move, too long of a distance")
			else: 
				for i in range(offramp1B,offramp1B+indexes):
					freeway[i, 0, 0] = NOT_USED
				for j in range(offramp1B+indexes,offramp1E+indexes):
					freeway[j, 0, 0] = OFF_RAMP
				for k in range(onramp1B+indexes,onramp1E+indexes):
					freeway[k, 0, 0] = ON_RAMP
		#Move on-ramp 2
		if(onRamp == ON_RAMP_TWO):
			if (indexes >= ramp2FrontMovement):
				print ("Can't move, too long of a distance")
			else: 
				for i in range(offramp2B,offramp2B+indexes):
					freeway[i, 0, 0] = NOT_USED
				for j in range(offramp2B+indexes,offramp2E+indexes):
					freeway[j, 0, 0] = OFF_RAMP
				for k in range(onramp2B+indexes,onramp2E+indexes):
					freeway[k, 0, 0] = ON_RAMP
		#Move on-ramp 3
		if(onRamp == ON_RAMP_THREE):
			if (indexes >= ramp3FrontMovement):
				print ("Can't move, too long of a distance")
			else: 
				for i in range(offramp3B,offramp3B+indexes):
					freeway[i, 0, 0] = NOT_USED
				for j in range(offramp3B+indexes,offramp3E+indexes):
					freeway[j, 0, 0] = OFF_RAMP
				for k in range(onramp3B+indexes,onramp3E+indexes):
					freeway[k, 0, 0] = ON_RAMP
	# Moves the specified on-ramp backwards
	if(direction == 'b' or direction == 'B'):
		#Move on-ramp 1
		if(onRamp == ON_RAMP_ONE):
			if (indexes >= ramp1RearMovement):
				print ("Can't move, too long of a distance")
			else: 
				for i in range(offramp1B-indexes,offramp1E-indexes):
					freeway[i, 0, 0] = OFF_RAMP
				for j in range(onramp1B-indexes,onramp1E-indexes):
					freeway[j, 0, 0] = ON_RAMP
				for k in range(onramp1E-indexes,onramp1E+indexes):
					freeway[k, 0, 0] = NOT_USED
		if(onRamp == ON_RAMP_TWO):
			if (indexes >= ramp2RearMovement):
				print ("Can't move, too long of a distance")
			else: 
				for i in range(offramp2B-indexes,offramp2E-indexes):
					freeway[i, 0, 0] = OFF_RAMP
				for j in range(onramp2B-indexes,onramp2E-indexes):
					freeway[j, 0, 0] = ON_RAMP
				for k in range(onramp2E-indexes,onramp2E+indexes):
					freeway[k, 0, 0] = NOT_USED
		if(onRamp == ON_RAMP_THREE):
			if (indexes >= ramp3RearMovement):
				print ("Can't move, too long of a distance")
			else: 
				for i in range(offramp3B-indexes,offramp3E-indexes):
					freeway[i, 0, 0] = OFF_RAMP
				for j in range(onramp3B-indexes,onramp3E-indexes):
					freeway[j, 0, 0] = ON_RAMP
				for k in range(onramp3E-indexes,onramp3E+indexes):
					freeway[k, 0, 0] = NOT_USED

def moveCarsChanged():
	global TIME_SECONDS
	global trackedCount
	global timeStepList
	while TIME_SECONDS + 1 < len(timeStepList):
		finishLine()
		moveCarsHelper()
		addAgentNewLayout()
		TIME_SECONDS += 1
		plt.axis('off')
		print(TIME_SECONDS)
		plt.figure(1)
		visualize()
		plt.pause(.0001)

###################################################################################
######## created a smaller freeway of size 20 by 4 for testing purposes###########
###################################################################################
global small_freeway
a = (20, 4, 4)
small_freeway = np.zeros(a, dtype = object)
def test_freeway():
	global small_freeway
	freeway[:, :, 2] = None # initilaize all cars to none
	freeway[:, 1:3, 0] = REGULAR
	freeway[:, 3, 0] = TOLL
	freeway[:, 0, 0] = NOT_USED
	freeway[:, :, 3] = CAN_CHANGE_LANES

	for i in range(freeway.shape[0]):  # placing vehicles on the map\
		for j in range(freeway.shape[1]):
			val = np.random.uniform(0, 1)
			if ((j == 1 or j == 2) and val < .5): # placing vehicles on regular lanes
				freeway[i][j][2] = car_agent.Car(i, j, False, TIME_SECONDS, speed)  
			elif (j == 3 and val < .25): # placing vehicles on toll lanes
				freeway[i][j][2] = car_agent.Car(i, j, False, TIME_SECONDS, speed)

def displayOutput():

	for i in range(len(list)):
		print("Agent", i + 1, ": ", round(list[i] / 60, 2), " minutes")
	print()
	print("*********************************************************************************************")
	print("*********************************************************************************************")
	print()

	if (len(tollList) == 0):
		print("No toll agents recorded")
	
	else:	
		for i in range(len(tollList)):
			print("Toll Agent", i + 1, ": ", round(tollList[i] / 60, 2), " minutes")

	print()
	print("*********************************************************************************************")
	print("*********************************************************************************************")
	print()

	array = np.array(list)
	tolArray = np.array(tollList)

	print ("Average time for a regular car to finish simulation: ", round(array.mean() / 60, 2), " minutes")

	if (len(tollList) != 0):
		print ("Average time for a toll lane car to finish simulation: ", round(tolArray.mean() / 60, 2), " minutes") 


# Initializes the basic road. 
initializeRoad()					
moveCars()
displayOutput()
TIME_SECONDS = 0
trackedCount = 0
list = []


####################################################
# Different layouts - Uncomment the freeway layout
# that you would like to use
####################################################
initializeExtraTollLane()				
#initializeEmpty()						
#makeTollRegular()						
#initializeExtraLane()					
moveCarsChanged()
displayOutput()
########################################