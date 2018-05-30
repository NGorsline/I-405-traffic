import numpy as np
import car_agent
np.set_printoptions(threshold=np.inf)
import math
#import tkinter
import matplotlib.pyplot as plt
import matplotlib.colors
import time
import math

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
global addedYet

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
percentReg = .50
percentTol = .25
percentOnramp = .1
onrampCount = 0
redLightSpeed = 8

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

# every 30 seconds we add a new tracked agent
trackedSpeed = 30 
trackedCount = 0
tollTrackedCount = 0
addedYet = False

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
	global REG_COUNT
	global TIME_SECONDS

	freeway[:, :, 2] = None # initilaize all cars to none
	freeway[:, 1:3, 0] = REGULAR
	freeway[:, 3, 0] = TOLL
	freeway[:, 0, 0] = NOT_USED
	freeway[:, :, 3] = CANNOT_CHANGE_LANES
	freeway[:, :, 1] = -3000

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

# Adds on and off ramps to the freeway
def AddingRampsToFreeway():
	for i in range(len(freeway)):
		val = np.random.uniform(0, 1)
		#setting the off ramps values to the freeway
		if (i >= offramp1B and i <= offramp1E) or (i >= offramp2B and i <= offramp2E) or (i >= offramp3B and i <= offramp3E) or (i >= offramp4B and i <= offramp4E):
			freeway[i, 0, 0] = OFF_RAMP
		 #setting the on ramps values to the freeway
		if (i >= onramp1B and i <= onramp1E) or (i >= onramp2B and i <= onramp2E) or (i >= onramp3B and i <= onramp3E):
			freeway[i, 0, 0] = ON_RAMP
			if (val < percentOnramp):
				freeway[i, 0, 2] = car_agent.Car(i, 0, False, TIME_SECONDS)
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
	for i in range(freeway.shape[0] - 1, -1, -1):
		for j in range(freeway.shape[1] - 1, -1, -1):
			if type(freeway[i, j, 2]) is car_agent.Car:
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
	
	for i in range(freeway.shape[1]):
		val = np.random.uniform(0, 1)
		hasSet = False
		if ((i == 1 or i == 2) and val < percentReg and freeway[0, i, 1] != TIME_SECONDS):
			freeway[0][i][2] = car_agent.Car(0, i, False, TIME_SECONDS)
			REG_COUNT += 1
			if (TIME_SECONDS % trackedSpeed == 0 and trackedCount < 30 and hasSet == False):
				addedYet = True
				freeway[0][i][2].tracked = True
				trackedCount += 1
				hasSet = True
		elif (i == 3 and val < percentTol and freeway[0, i, 1] != TIME_SECONDS):
			freeway[0, i, 2] = car_agent.Car(0, i, False, TIME_SECONDS)
			TOL_COUNT += 1
			if (TIME_SECONDS % trackedSpeed == 0 and trackedCount < 30 and hasSet == False):
				addedYet = True
				freeway[0][i][2].tracked = True
				tollTrackedCount += 1
				hasSet = True

	# adding cars to the on ramps
	if (TIME_SECONDS % redLightSpeed == 0):
		freeway[onramp1B][0][2] = car_agent.Car(onramp1B, 0, False, TIME_SECONDS)
		freeway[onramp2B][0][2] = car_agent.Car(onramp2B, 0, False, TIME_SECONDS)
		freeway[onramp3B][0][2] = car_agent.Car(onramp3B, 0, False, TIME_SECONDS)
		freeway[offramp4B][0][2] = car_agent.Car(offramp4B, 0, False, TIME_SECONDS)

def moveCars():
	global TIME_SECONDS
	global trackedCount
	while len(list) != 30:
		removeVehicleFromExitLane()
		finishLine()
		moveCarsHelper()
		addAgent()
		TIME_SECONDS += 1
		plt.figure(1)
		visualize()
		plt.pause(.0001)
		#plt.figure(2)
		#congestionVis()
		#plt.pause(.0001)

#Removes vehicles from the map once they reach the finish line 
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
			if freeway[i + 800][j][2] == None:
				carVis[i][j] = 900
			if type(freeway[i + 800][j][2]) is car_agent.Car:
				carVis[i][j] = 100
				if freeway[i + 800, j, 2].is_tracked():
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


#################
#Calling Methods# 
#################

initializeRoad()
AddingRampsToFreeway()
markAvailableSpaces()
moveFreewayOnRamp(ON_RAMP_ONE,"F",400)
moveCars()

#test_freeway()
#######################################################
#######################################################


####################################################################
# Prints!											  			   #	
####################################################################
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
