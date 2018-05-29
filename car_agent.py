import numpy.random as np_rand

class Car:
	MAX_SPEED = 6
	MIN_SPEED = 0
	SPEED_PER = 10.22 # mph per speed step
	# the index which holds the car value in the freeway grid
	CAR_INDEX = 2 
	# index that holds the time value in the freeway grid 
	TIME_INDEX = 1
	# index that holds the lane type value in the freeway grid 
	LANE_TYPE_INDEX = 0
	# index that holds the time value in the freeway grid 
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

	# Percent chance of a car hopping onto the toll lane
	PERC_CHANGE_TOLL = .2
	# Percent chance of a car speeding up next to an on-ramp cuz it sees a car next to it
	PERC_SPEED_UP = .6
	# percent of a car in the toll lane switching out of it
	PERC_OUT_OF_TOLL = .05
	
	
   # Constructor 
	def __init__(self, row, col, tracked, st):
		# class variables
		self.speed = 0  # TEMP SET TO 0 # will be set when the car is created
		self.row = row # location that the vehicle is currently at
		self.col = col # location that the vehicle is currently at
		self.completed = False # If the car has left the simulation
		self.starting_time = st  # will be set when car is spawned into the sim
		self.finishing_time = None  # will be set when car passes the end of the road
		self.tracked = tracked # boolean indicating that this car is tracked

	def is_tracked(self):
		return self.tracked

	def start_time(self):
		return self.starting_time

	'''
		The running function of the whole car_agent class
		This function will be called on each index that has a car in it
		as the grid loops through
	'''
	def drive(self, grid, sim_time):
		#################################### SOME PSEUDOCODE MADE by TRAN 
		###### LET'S USE A SWITCH STATEMENT TO IMPLIMENT THIS <--------- python does not have switch cases apparently
		curr_car = grid[self.row, self.col, self.LANE_TYPE_INDEX]
		# if this car is in the regular lane
		if (curr_car == self.REGULAR):
			pass
			# it might change lane by 30%
				# within change lane function, the car might go into the toll lane by 20% if it's next to a dotted line section
				# 80% it will go straight

		# if this regular lane car is NEXT to the toll lane
		if (curr_car == self.REGULAR and\
			grid[self.row, self.col + 1, self.LANE_TYPE_INDEX] == self.TOLL):
			self.change_into_toll(grid, sim_time)
			# it might try and get into it by a certain percentage?
				
		# if this regular lane car is NEXT TO an exit, it might exit by the percentage specified at that exit??? 
		if (curr_car == self.REGULAR and \
			grid[self.row + 1, self.col - 1, self.LANE_TYPE_INDEX] == self.OFF_RAMP):
			pass

		# if this regular lane car is NEXT TO an on ramp
		if (curr_car == self.REGULAR and grid[self.row, self.col - 1, self.LANE_TYPE_INDEX] == self.ON_RAMP):
			pass
			# WE CAN HAVE 2 "algorithm"
				# 1. it wouldn't give a fuck and keep going on its marry way cuz on-ramp cars are supposed to merge onto freeway
				# 2. call self.next_to_ramp(freeway) function
					# it'll have a chance of speeding up or slowing down
			# FANCY FEATURE: if this car is next to an on ramp, and a car is right "next" to it on the on ramp, 
							# it'll either increase its speed by whatever_the_other_car_speed_is+2, or slow down by whatever_the_other_car_speed_is-1
							# JKKK THIS IS SHITTY I DON'T WANNA DO IT
				
		# if this car is in the toll lane
		if (curr_car == self.TOLL):
			pass
			# it might change out if it's at a dotted line section by 5%????? i'm pulling 5% out of my ass
			# else i'll go straight
			# it might change lanes if there are more than 2 toll lanes
			#

		# if this car is on the on-ramp
		if (curr_car == self.ON_RAMP):
			pass
			# if the 
			# it will move to the end of the ramp and attempt to merge if there's an open space
				# by calling nick's move_forward function last
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
		car_speed = 6

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

	''' 
	checking if the index passed in is an index I can change into
	THIS COuld just be changed into just returning what is in the if 
	check paraenthesis thing
	but that's ok....
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

	'''
		This function takes care of :
		 - checking if the space is in bound 
		 - if the lane could be changed into
		 - changing into a toll lane   <-------- it might not do this, i sorta wanna move it into another funciton
		 - making sure time stamp is correct
		
		Parameter:
			- freeway: the 3d array
			- sim_time: the current time but not really

		Assumptions:
			- not sure yet

		Problem: 
			- I want to move cars that want to change into a toll lanes for a seperate function
	'''
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
					if (freeway[self.row + i, left_lane_col, self.CAR_INDEX] == None): 
						left_availability += 1

				# right lane
				if (valid_right_lane):
					if (freeway[self.row + i, right_lane_col, self.CAR_INDEX] == None): 
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

		#***************************************8
		index_to_check = freeway[potential_space_switch_row, potential_space_switch_col]
		# Check if it's a regular lane, and if the time stamp is ok
		if (index_to_check[self.LANE_TYPE_INDEX] == self.REGULAR and \
			index_to_check[self.TIME_INDEX] < sim_time):
			self._move_to_new(freeway, potential_space_switch_row, potential_space_switch_col, sim_time)
			# CHANGE SPEED of THE CAR
			if (self.speed < self.MAX_SPEED): 
				self.speed += 1
				return None
		
		# #########################IT MIGHT NOT MAKE SENSE TO DO THIS, IT SHOULD BE A FUNCTION#############################
		# DON'T FORGET to ooo REMOVEEEE A CAR ONCE YOU'VE MOVED IT *****************************8
		# ######**** THE FUNCTION BELOW WAS MOVED INTO ITS OWN METHOD 
		# # ****CHANGING INTO TOLL LANE
		# if (index_to_check[self.LANE_TYPE_INDEX] == self.TOLL and \
		# 	index_to_check[self.CHANGE_L_INDEX] == True and \
		# 	index_to_check[self.TIME_INDEX] < sim_time):
		# 	rand_num = np_rand.uniform(0.0, 1.0)
		# 	if (rand_num <= self.PERC_CHANGE_TOLL):
		# 		self._move_to_new(freeway, potential_space_switch_row, potential_space_switch_col, sim_time)
		# 		if (self.speed < self.MAX_SPEED): 
		# 			self.speed += 1
		# 			return None
		# 	# else if you didn't get under the random values, the car will just stay in the lane where it's at
		# 	else:
		# 		self.move_forward(freeway, sim_time)
		
	'''
		function for cars that are next to the toll lane and
		it may or may not want to get into it (by chance)
		

		Assumption: 
			- This car is already next to a toll lane that's at a section where you can change into
			and out of
	'''
	def change_into_toll(self, freeway, sim_time):
		pot_row = self.row + 1
		pot_col = self.col + 1
		rand_num = np_rand.uniform(0.0, 1.0)
		if (freeway[self.row + 1, self.col + 1, self.CAR_INDEX] == None):
			if (rand_num <= self.PERC_CHANGE_TOLL):
				self._move_to_new(freeway, pot_row, pot_col, sim_time)
				if (self.speed < self.MAX_SPEED): 
						self.speed += 1
						return None
			# else move forward 
			else:
				self.move_forward(freeway, sim_time)

	'''
		Cars that are in the toll lane wanting to switch out of it
		the function will also cover not meeting the chance of wanting to 
		change and instead it will just go straight

		Assumption: 
			- The car is already in a toll lane that's rightest (which means it's near the regular lane)
				---> this means it's in the left lane if you're talking bout our grid cuz the grid is upside down
	'''
	def toll_car_change_out(self, freeway, sim_time):
		space_to_check_row = self.row + 1  # + 1 because it's checking a diagonal space
		space_to_check_col = self.col - 1  # -1 because the lane it's checking is to its left on the grid
		space_to_check = freeway[space_to_check_row, space_to_check_col]
		# check if the space next to this car and see if it could change lane into
		if (freeway[self.row, self.col, self.CHANGE_L_INDEX] == True and \
			space_to_check[self.CAR_INDEX] == None and \
			space_to_check[self.LANE_TYPE_INDEX] == self.REGULAR):
			rand_num = np_rand.uniform(0.0, 1.0)
			# if it meeets the percent of it changing out of toll lane, it'll move to its open new space
			if (rand_num <= self.PERC_OUT_OF_TOLL):
				self._move_to_new(freeway, space_to_check_row, space_to_check_col, sim_time)
				if (self.speed < self.MAX_SPEED):
					self.speed += 1
			# else it'll just move forward
			else:
				self.move_forward(freeway, sim_time)

	'''
		For cars that are in the toll lane and want to change lane internally
		---> actually i don't think i need this
		i can just call the change lane function
	'''
	def toll_car_change_lane(self, freeway, sim_time):
		pass

	'''
		Function for car on the freeway next to an on ramp
		to slow down for the car on the on ramp to be able to get
		on to the freeway
			

		Parameter:
			freeway - the 3d array that represents the freeway and its values

		Assumption:
			The car is currently next to an on-ramp

		PROBLEM:
			- this function does not yet take care of situations where there'd be 
			2+ on-ramp lanes that merges into one
	'''
	def next_to_ramp(self, freeway):
		# ramps are to the left
		on_ramp_col = self.col - 1
		if (on_ramp_col >= 0):
			# if there's a car next to it 
			car_on_ramp = freeway[self.row, on_ramp_col, self.CAR_INDEX] 
			if (car_on_ramp != None):
				# if they're going at the same speed
				if (car_on_ramp.speed == self.speed):
					# there's a chance the car on the freeway will speed up
					rand_num = np_rand.uniform(0.0, 1.0)
					# SPEED UP
					if (rand_num <= self.PERC_SPEED_UP): 
						if (self.speed < self.MAX_SPEED):
							self.speed -= 1
					# SLOW Down
					else:
						if (self.speed > self.MIN_SPEED):
							self.speed += 1


	'''
		Function for cars that are at the end of the ramp
		and want to merge onto the freeway
		This merge will be diagonally, not horizontally

		Parameter: 
			freeway - the 3d array that represents the freeway and its values
		
		Assumption:
			- the car is already at the end of the ramp
			- there's a lane to its right
		
		PROBLEM:
			- i'm currently checking the time of the space i'm moving to
				do i care???
	'''
	def merge_onto_freeway(self, freeway, sim_time):
		open_space_row = self.row + 1
		open_space_col = self.col + 1
		index_to_check = freeway[open_space_row,open_space_col]
		if (index_to_check[self.CAR_INDEX] == None and  \
			index_to_check[self.TIME_INDEX] < sim_time and \
			index_to_check[self.CHANGE_L_INDEX] == True):  # ****************SHOULD THIS BE LESS THAN AND EQUAL TO
			self._move_to_new(freeway, open_space_row, open_space_col, sim_time)

	'''
		i probably don't need this,
		can just call nick's move_forward function
	'''
	def on_ramp_move_forward(self, freeway):
		pass

	'''
		Helper function that's called by _move_to_new()
		I don't have to do it this way but...
		whatever
	'''
	def _set_location(self, row, col):
		self.row = row
		self.col = col

	'''
		- Drop a time poop of where it is at right now
		- deleting it from where it is at right now
		- Move this current car to a new row col
		- Update where it moved to time stamp
		
		Parameter: 
			- the freeway
			- new_row and new_col is the new location
			- the current simulation time so time could be updated correctly
	'''
	def _move_to_new(self, freeway, new_row, new_col, sim_time): 
		freeway[new_row, new_col, self.CAR_INDEX] = freeway[self.row, self.col, self.CAR_INDEX]
		freeway[new_row, new_col, self.TIME_INDEX] = sim_time + 1
		freeway[self.row, self.col, self.CAR_INDEX] = None
		freeway[self.row, self.col, self.TIME_INDEX] = sim_time

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
	'''
		NICK GIVE SOME DESCRIPTION
		Problem: 
			- not taking care of the case where the car might move onto a -1 lane type space
				-->> these are for on ramp situations 
			
	'''
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
					self.speed += 1
		
		else:
			val = self._get_next_available_location(grid, sim_time)
			if val < self.speed:
				self._move_to_new(grid, self.row + val, self.col, sim_time)
			else:
				self._move_to_new(grid, self.row + self.speed, self.col, sim_time)
				self.speed += 1