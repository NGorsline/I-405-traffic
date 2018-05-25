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


	def drive(self, grid, sim_time):
		#################################### SOME PSEUDOCODE MADE by TRAN 
		# if this car is in the regular lane
			# it might change lane by 30%
				# within change lane function, the car might go into the toll lane by 20% if it's next to a dotted line section
				# 70% it will go straight
			# if this regular lane car is next to an exit, it might exit by the percentage specified at that exit??? <--- IS THIS TOO FANCY
			# FANCY FEATURE: if this car is next to an on ramp, and a car is right "next" to it on the on ramp, 
							# it'll either increase its speed by whatever_the_other_car_speed_is+2, or slow down by whatever_the_other_car_speed_is-1
							# JKKK THIS IS SHITTY I DON'T WANNA DO IT
		# if this car is in the toll lane
			# it might change out if it's at a dotted line section by 5%????? i'm pulling 5% out of my ass
			# else i'll go straight

		# if this car is on the on-ramp
			# it will move to the end of the ramp and attempt to merge if there's an open space
			# johnny boi wants some type of look ahead by the cars in the main road, but fuck that right?
			# ---> shit's too fancy
		####################################	
		# change lane   <-- TRAN
		# if thIS car is in the toll lane and it's at a spot where it could switch out of 
				# it might just do it FOR SOME CHANCE
		# move foward (accelerate and decelerate accordingly)
		self.move_forward(grid, sim_time)
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
			if (freeway[row + i, col, self.CAR_INDEX] != None):
				return freeway[row + i, col, self.CAR_INDEX].speed
		return car_speed
		  

	''' checking if the colume (lane) passed in is in bound
	Parameter: 
		lane - column index
	'''
	def _lane_in_bound(self, lane):
		if (lane >= 0 and lane < self.NUM_LANES):
			return True
		return False

	''' checking if the index passed in is an index I can change into
	Parameters:
		freeway - the grid that represents the freeway
		row - obvious
		col - obvious
	'''
	def _can_change_into(self, freeway, row, col):
		if ((freeway[row, col, self.LANE_TYPE_INDEX] != self.NOT_USED) and \
			(freeway[row, col, self.LANE_TYPE_INDEX] != self.ON_RAMP) and \
			(freeway[row, col, self.LANE_TYPE_INDEX] != self.OFF_RAMP)):
			return True
		return False

	def change_lane(self, freeway, sim_time):
		# ****************************DO SOME BOUNDARY CHECKING ***********************!!!!!!
		# SOME HOT VARIABLES 
		left_availability = 0
		right_availability = 0
		space_needed = (self.speed%10)  # space travel within a second based on currently speed
		left_lane_col = self.col - 1
		right_lane_col = self.col + 1
		
		# Checking if the right and left lanes are in bound
		# and if they are, is it a lane that could be changed into
		left_lane_in_bound = self._lane_in_bound(left_lane_col)  # true or false
		valid_left_lane = left_lane_in_bound and self._can_change_into(freeway, self.row, left_lane_col)

		right_lane_in_bound = self._lane_in_bound(right_lane_col)  # true or false
		valid_right_lane = right_lane_in_bound and self._can_change_into(freeway, self.row, right_lane_col)

		# check if the path to where i'll be in both lane is clear
		# +1 because value in range is exclusive
		# and start at 1 because i don't care to check for the space next to me
		# the change lane will happen diagonally
		for i in range(1, space_needed + 1):  
			# if row + i is within the grid
			if (self.row + i <= self.LAST_INDEX):
				if (valid_left_lane):
					# if the current index being check does not have a car in it
					if (freeway[self.row + i, left_lane_col, self.CAR_INDEX] != None): 
						left_availability += 1

				# right lane
				if (valid_right_lane):
					if (freeway[self.row + i, right_lane_col, self.CAR_INDEX] != None): 
						right_availability += 1

		# it's giving preference for right lane... like real life ;)
		# it might not get into this if elif if block at all 
		# if that happens, the car will just keep driving moving forward.
		if (right_availability >= left_availability and right_availability == space_needed):
			potential_space_switch_row = self.row + space_needed
			potential_space_switch_col = right_lane_col
		elif (left_availability >= right_availability and left_availability == space_needed):
			potential_space_switch_row = self.row + space_needed
			potential_space_switch_col = left_lane_col
		else: 
			self.move_forward(freeway, sim_time)
			return None # is this okay? Could I just have a return nothing

		# #########################IT MIGHT NOT MAKE SENSE TO DO THIS, IT SHOULD BE A FUNCTION#############################
		# DON'T FORGET to ooo REMOVEEEE A CAR ONCE YOU'VE MOVED IT *****************************8
		# 20% CHANCE OF GETTING IN TO TOLL LANE   
		# ****CHANGING INTO TOLL LANE
		if (freeway[potential_space_switch_row, potential_space_switch_col, self.LANE_TYPE_INDEX] == self.TOLL and \
			freeway[potential_space_switch_row, potential_space_switch_col, self.CHANGE_L_INDEX] == True):
			randNum = np_rand.uniform(0.0, 1.0)
			if (randNum <= self.PERC_CHANGE_TOLL):
				self._move_to_new(freeway, potential_space_switch_row, potential_space_switch_col)
			# else if you didn't get under the random values, the car will just stay
			else:
				self.move_forward(freeway, sim_time)
		
		# REGULAR GUYS
		if (freeway[potential_space_switch_row, potential_space_switch_col, self.LANE_TYPE_INDEX == self.REGULAR]):
			self._move_to_new(freeway, potential_space_switch_row, potential_space_switch_col)
		# CHANGE SPEED of THE CAR
		if (self.speed < self.MAX_SPEED): 
			self.speed += 1

	'''Cars that are in the toll lane wanting to switch out of it
	the function will also cover not meeting the chance of wanting to change and instead it will just go straight
	'''
	def toll_car_change_l(self, freeway):
		


	'''
		Moves this current car to a new row col, deleting it from where it is at right now
		Parameter: new_row and new_col is the new location
	'''	
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

	def _get_next_available_location(self, grid, sim_time):
		index_free = 0
		# Loop from one in front to 6 in front
		for i in range(1, 7): 
			row_to_check = self.row + i
			grid_to_check = grid[row_to_check, self.col]
			if row_to_check < self.LAST_INDEX and sim_time != grid_to_check[self.TIME_INDEX] and grid_to_check[self.CAR_INDEX] == None:
				index_free = index_free + 1
			else:
				break
		return index_free

	# This method will attempt to move the vehicle forward
	def move_forward(self, grid, sim_time):

		grid[self.row, self.col, self.TIME_INDEX] = sim_time

		# Create helper function to check if the spaces in front will be clear at the speed traveled
		if self.speed == 0 and self.row < self.LAST_INDEX: 
			# Dropping current time to spot at to update for next agent if needed
			new_row = self.row + 1
			new_col = self.col
			# Check to see if the proposed new spot has a car at that location or had one on the same time stamp
			if grid[new_row, new_col, self.CAR_INDEX] == None and grid[new_row, new_col, self.TIME_INDEX] != sim_time:
				# Create helper to move car from source location to target location
				grid[new_row, new_col, 2] = grid[self.row, self.col, 2]
				grid[self.row, self.col, 2] = None
				self._set_location(new_row, new_col)
				if(self.speed < self.MAX_SPEED):
					#self.speed += 1
					pass #for now
		
		# this else will never be hit
		else:
			
			val = self._get_next_available_location(grid, sim_time)
			if val < self.speed:
				self._move_to_new(grid, self.row + val, self.col)
			else:
				self._move_to_new(grid, self.row + self.speed, self.col)
				self.speed += 1
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


