import numpy as np
import car_agent
np.set_printoptions(threshold=np.inf)
import math

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
LINES = 5
#Represents locations of the freeway where a car is not allowed to drive in
NOT_USED = -1
#Represents the total number of indexes we need to represent 6.8 miles.
#Each index represent 15 feet.
MILES = 2320  

attributeList = [0, False, "Car"]
aList = np.array(attributeList)
s = (MILES< 4, 4)
freeway = np.zeros(s, dtype = object)

#The freeway is represented as a 2D array
def initializeRoad():
    global freeway
    freeway[:, 1:3, 0] = REGULAR
    freeway[:, 3, 0] = TOLL
    freeway[:, 0, 0] = NOT_USED
    freeway[:, :, 1] = False

    for i in range(freeway.shape[0]):  # placing vehicles on the map
        for j in range(freeway.shape[1]):
            val = np.random.uniform(0, 1)
            if ((j == 1 or j == 2) and val < .5): # placing vehicles on regular lanes
                freeway[i][j][2] = "c"  # JUST A STING FOR NOW SINCE TRAN HASN'T DONE THE CLASS YET AND I DONT WANNA FUCK SHIT UP
            elif (j == 3 and val < .25): # placing vehicles on toll lanes
                freeway[i][j][2] = "c"

# Adds the on and off ramps to the freeway
def AddingRampsToFreeway():
    for i in range(len(freeway)):
         #setting the off ramps value to the freeway
         if (i >= 774 and i <= 844) or (i >= 1547 and i <= 1653) or (i >= 1794 and i <= 1900):
              freeway[i, 0, 0] = OFF_RAMP
         #setting the on ramps value to the freeway
         if (i >= 845 and i <= 951) or (i >= 1654 and i <= 1724) or (i >= 1901 and i <= 2042) or (i >= 2213 and i <= 2320):
              freeway[i, 0, 0] = ON_RAMP

initializeRoad()
AddingRampsToFreeway()

print(freeway)
