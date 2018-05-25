import numpy.random as np_rand

class Car:
	MAX_SPEED = 6
	SPEED_PER = 10.22 # mph per speed step
	CAR_INDEX = 2  # the index which holds the car value
	TIME_INDEX = 1
	LANE_TYPE_INDEX = 0
	CHANGE_L_INDEX = 3

	# numbers for initializing the grid
	NUM_LANES = 4 
	LAST_INDEX = 2320-1

	#Represents regular lanes in the freeway
	REGULAR = 1
	#Represents the off ramp on the freeway
	OFF_RAMP = 2
	#Represents the toll lane on the freeway
	TOLL = 3
	ON_RAMP = 4
	# Value that represents this lane is not used, it's not a lane at all...
	NOT_USED = -1
	PERC_CHANGE_TOLL = .2  # 20%
	
	
   # Constructor 
	def __init__(self, row, col, tracked):
		# class variables
		self.speed = 0  # TEMP SET TO 0 # will be set when the car is created
		self.row = row # location that the vehicle is currently at
		self.col = col # location that the vehicle is currently at
		self.completed = False # If the car has left the simulation
		self.starting_time = None  # will be set when car is spawned into the sim
		self.finishing_time = None  # will be set when car passes the end of the road
		self.tracked = tracked # boolean indicating that this car is tracked

	def is_tracked(self):
		return self.tracked

	def _set_location(self, row, col):
		self.row = row
		self.col = col


	def drive(self, grid):
	   # change lane   <-- TRAN
	   # move foward (accelerate and decelerate accordingly)
	   self.move_forward(grid)
	   # enter toll lane if near it (by a percent)
	   # exit if near exit (by a percent)
	   # stay 


	# TRAN'S SECTION#########################################################3
	# helper function for change_lane
	# it returns the speed of the car in front of the parameter row col 
	# and in front as in however many spaces in front
	# if it does not find a car, it'll just return max speed which is 60
	def _closest_car_in_front_speed(self, freeway, row, col):
		# search for the nearest car
		space_needed = (self.speed%10) - 1
		car_speed = 60.0

		for i in range(6 - space_needed): 
			if (freeway[row + i, col, self.CAR] != None):
				return freeway[row + i, col, self.CAR].speed
		return car_speed
		  

	def _is_lane_out_of_bound(self, lane):
		if (lane >= 0 and lane < self.NUM_LANES):
			return True
		return False

	# checking for if
	def _can_change_into(self, freeway, row, col):
		if ((freeway[row, col, self.LANE_TYPE_INDEX] != self.NOT_USED) and \
			(freeway[row, col, self.LANE_TYPE_INDEX] != self.ON_RAMP) and \
			(freeway[row, col, self.LANE_TYPE_INDEX] != self.OFF_RAMP)):
			return True
		return False

	def change_lane(self, freeway):
		# ****************************DO SOME BOUNDARY CHECKING ***********************!!!!!!
		# SOME HOT VARIABLES 
		left_availability = 0
		right_availability = 0
		space_needed = (self.speed%10)  # space travel within a second based on currently speed
		left_lane_col = self.col - 1
		left_lane_in_bound = self._is_lane_out_of_bound(left_lane_col)
		right_lane_col = self.col + 1
		right_lane_in_bound = self._is_lane_out_of_bound(right_lane_col)

		# check if the path to where i'll be in both lane is clear
		# +1 because value in range is exclusive
		# and start at 1 because i don't care to check for where i am currently at 
		for i in range(1, space_needed + 1):  
			
			if (self.row + i <= self.LAST_INDEX):
				# left lane
				if (left_lane_in_bound):
					if (freeway[self.row + i, left_lane_col, self.CAR_INDEX] != None and \
						self._can_change_into(freeway, row + i, left_lane_col)): 
						left_availability += 1

				# right lane
				if (right_lane_in_bound):
					if (freeway[self.row + i, right_lane_col, self.CAR_INDEX] != None and \
						self._can_change_into(freeway, row + i, right_lane_col)): 
						right_availability += 1

		# it's giving preference for right lane... like real life ;)
		if (right_availability >= left_availability):
			potential_space_switch_row = self.row + space_needed
			potential_space_switch_col = right_lane_col
		elif (left_availability >= right_availability):
			potential_space_switch_row = self.row + space_needed
			potential_space_switch_col = left_lane_col
		
		# #########################IT MIGHT NOT MAKE SENSE TO DO THIS, IT SHOULD BE A FUNCTION#############################
		# DON'T FORGET to ooo REMOVEEEE A CAR ONCE YOU'VE MOVED IT *****************************8
		# 20% CHANCE OF GETTING IN TO TOLL LANE   
		# ****CHANGING INTO TOLL LANE
		if (freeway[potential_space_switch_row, potential_space_switch_col, self.LANE_TYPE_INDEX] == self.TOLL and \
			freeway[potential_space_switch_row, potential_space_switch_col, self.CHANGE_L_INDEX] == True):
			randNum = np_rand.uniform(0.0, 1.0)
			if (randNum <= self.PERC_CHANGE_TOLL):
				_move_to_new(freeway, potential_space_switch_row, potential_space_switch_col)
			# else if you didn't get under the random values, the car will just stay
			else: 
				continue
		if (freeway[potential_space_switch_row, potential_space_switch_col, self.LANE_TYPE_INDEX == self.REGULAR]):
			one = 1 # TEMPEROJRARRARYRYYYY
		
	

		# CHANGE SPEED of THE CAR 
		
	def _move_to_new(self, freeway, new_row, new_col): 
		freeway[new_row, new_col, self.CAR_INDEX] = freeway[self.row, self.col, self.CAR_INDEX]
		freeway[self.row, self.col, self.CAR_INDEX] = None
		self._set_location(new_row, new_col)

	# each freeway exit has a different percent that the driver will take it
	# each freeway exit has only once cell in which a car can exit, and once it has
	#     entered the exit ramp, it can not change its mind (will be forced to exit)
	# -- 30% for Bothell-Mill Creek (maybe exit 26)
	# -- 10% for all other
	def exit_freeway(self, grid):
		# potential_space to exit <-- variable
		# generate random number and compare to exit percent
		# If randomly generated percentage is within the exit range
		#    take the exit and remove car from simulation after it reaches the end of the ramp
		# Else
		#    Do not take the exit and continue to move forward if there is room
		pass

	def _get_next_available_location(self, grid):


	# This method will attempt to move the vehicle forward
	def move_forward(self, grid):

		# Create helper function to check if the spaces in front will be clear at the speed traveled
		if self.speed == 0 and self.row < LAST_INDEX: ## SECOND AND IS TEMP
			new_row = self.row + 1
			new_col = self.col
			# Check to see if the proposed new spot has a car at that location
			if grid[new_row, new_col, 2] == None: # ADD AN AND TO CHECK IF THE CAR WAS JUST THERE
				# Create helper to move car from source location to target location
				grid[new_row, new_col, 2] = grid[self.row, self.col, 2]
				grid[self.row, self.col, 2] = None
				self._set_location(new_row, new_col)
		for i in range(self.speed):
			pass
		# Check to see the speed of the car and if the car will encounter a space
		#    that has already been occupied in this time stamp (within the same second)
		# If the proposed space is open, and there are no cars or previosly occupied spots
		# in that path
		#	 The car can move forward
		# Else if the car will encounter a vehicle
		#	 then it will go as close as it can to the car infront without
		#	 going on the same spot, or on a spot previously occupied that time stamp
		# Else
		#	 Stay still, cannot move
		pass


