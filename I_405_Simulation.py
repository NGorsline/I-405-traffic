import numpy as np
import car_agent
np.set_printoptions(threshold=np.inf)
import math

global freeway

#Constants
REGULAR = 1
EXIT = 2
TOLL = 3
ON_RAMP = 4
LINES = 5
NOT_USED = -1
MILES = 2320


attributeList = [0, False, "Car"]
aList = np.array(attributeList)
s = (MILES, 4, 3)
freeway = np.empty(s)


#The freeway is represented as a 2D array

def initializeRoad():
    global freeway
    freeway[:, 1:3, 0] = REGULAR
    freeway[:, 3, 0] = TOLL
    freeway[:, 0, 0] = NOT_USED

    for i in range(freeway.shape[0]):  # placing vehicles on the map
        for j in range(freeway.shape[1]):
            val = np.random.uniform(0, 1)
            if ((j == 1 or j == 2) and val < .5): # placing vehicles on regular lanes
                freeway[i][j][1] = True
                freeway[i][j][2] = "Car"  # JUST A STING FOR NOW SINCE TRAN HASN'T DONE THE CLASS YET AND I DONT WANNA FUCK SHIT UP
            elif (j == 3 and val < .15): # placing vehicles on toll lanes
                freeway[i][j][1] = True
                freeway[i][j][2] = "Car"


initializeRoad()

print(freeway)