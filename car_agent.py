'''
	TODO:
	- ARE CARS WHEN SPAWNED IN GIVEN A SPEED? NOT RIGHT NOWWW WTFFFF
	- 
'''
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
	PERC_CHANGE_TOLL = .001
	# Percent chance of a car speeding up next to an on-ramp cuz it sees a car next to it
	PERC_SPEED_UP = .6
	# percent of a car in the toll lane switching out of it
	PERC_OUT_OF_TOLL = .001
	# percent of a car in the regular lane switching lane FIXME:: i'm pulling this number out of my ass
	PERC_REG_SWITCH_LANE = .2
	# percent chance of a car exiting 
	PERC_EXIT = .1  #FIXME: I'M puLLIng this out of my ass
	PERC_REG_SWITCH_LANE = .05
	
   # Constructor 
	def __init__(self, row, col, tracked, start_time, speed):
		# class variables
		self.speed = speed  # TEMP SET TO 0 # will be set when the car is created
		self.row = row # location that the vehicle is currently at
		self.col = col # location that the vehicle is currently at
		self.completed = False # If the car has left the simulation
		self.starting_time = start_time  # will be set when car is spawned into the sim
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

		- I return in every if or else block because I only want one thing to be executed on this
		car at a time
	'''
	def drive(self, grid, sim_time):
		#################################### SOME PSEUDOCODE MADE by TRAN 
		###### LET'S USE A SWITCH STATEMENT TO IMPLIMENT THIS <--------- python does not have switch cases apparently
		curr_car = grid[self.row, self.col, self.LANE_TYPE_INDEX]
		rand_num = np_rand.uniform(0.0, 1.0)
		# if this car is in the regular lane
		if (curr_car == self.REGULAR):
			## if it's next to a toll lane and it's a section the car could get into
			## it might hop on in to the toll lane
			#if (grid[self.row, self.col + 1, self.LANE_TYPE_INDEX] == self.TOLL and \
			#	grid[self.row, self.col + 1, self.CHANGE_L_INDEX] == True):
			#	self.change_into_toll(grid, sim_time)
			#	return None  # TIP: apparently you can do just return and that's implicitly means return None
			## TODO: WE CAN HAVE 2 "algorithm"
			#	# 1. it wouldn't give a fuck and keep going on its marry way cuz on-ramp cars are supposed to merge onto freeway
			#	# 2. call self.next_to_ramp(freeway) function
			#		# it'll have a chance of speeding up or slowing down
			## FANCY FEATURE: if this car is next to an on ramp, and a car is right "next" to it on the on ramp, 
			## else if it's next to an on ramp
			#elif (grid[self.row, self.col - 1, self.LANE_TYPE_INDEX] == self.ON_RAMP):
			#	self.next_to_ramp(grid, sim_time)  # <-- might slow down, sepeed up, or keep moving forward
			#	return
			## it might look into switching lane by a percentage that you can change
			if (rand_num <= self.PERC_REG_SWITCH_LANE):
				self.change_lane(grid, sim_time)  # <-- within this function, it might switch lane or it might go forward
				return
			else: 
				self.move_forward(grid, sim_time)
				return
		
		# CHECK POINT <------------------------- 
		# # if this regular lane car is NEXT TO an exit, it might exit by the percentage specified at that exit??? 
		# # TODO: move this into the regular car action when ready
		# if it's next to an off ramp
		# if (grid[self.row + 1, self.col-1, self.LANE_TYPE_INDEX] == self.OFF_RAMP):
		#	if (rand_num <= self.PERC_EXIT):
		#		self.exit_freeway(grid, sim_time)
		# 	pass
		
		
		# if this car is in the toll lane
		# ASSUMPTION: only the leftest toll lane will have the true variable
		# TODO: NOT YET implimented within toll lane switching lanes <--- FIXME: actually i might not care at all
		if (curr_car == self.TOLL):
			# if the toll lane car is at a spot where it could leave the toll lane
			if (grid[self.row, self.col, self.CHANGE_L_INDEX] == True and \
				rand_num <= self.PERC_OUT_OF_TOLL):
					self.toll_car_change_out(grid, sim_time)  # <--- within this function, it might go straight
					return
			# else if it's a spot where it can't switch out of 
			else: 
				self.move_forward(grid, sim_time)
				return
			
		# if this car is on the on-ramp
		if (curr_car == self.ON_RAMP):
			# if it's at a spot where it could switch out of
			if (grid[self.row, self.col + 1, self.CHANGE_L_INDEX] == True):
				self.merge_onto_freeway(grid, sim_time)
				return
			# else it's at a spot where it can't switch out 
			else:
				self.move_forward(grid, sim_time)
				return
			# it will move to the end of the ramp and attempt to merge if there's an open space
				# by calling nick's move_forward function last
	
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
		  

	''' 
		checking if the colume (lane) passed in is in bound
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
			(freeway[row, col, self.LANE_TYPE_INDEX] != self.OFF_RAMP) and \
			freeway[row, col, self.LANE_TYPE_INDEX] != self.TOLL):
			return True
		return False

	'''
		This function takes care of :
		 - checking if the space is in bound 
		 - if the lane could be changed into
		 - making sure time stamp is correct for it to switch into
		 - MOVE FORWARD if it does not meet the chance of changing lanes
		
		Parameter:
			- freeway: the 3d array
			- sim_time: the current time but not really

		Assumptions:
			- This is a regular car switching lane

		TODO:: 
			- [FIXED] I want to move cars that want to change into a toll lanes for a seperate function
	'''
	def change_lane(self, freeway, sim_time):
		# ****************************DO SOME BOUNDARY CHECKING[DONE] ***********************!!!!!!
		# SOME HOT VARIABLES 
		left_availability = 0
		right_availability = 0
		# space travel within a second based on currently speed (actually i didn't need this, max speed is)
		space_needed = (self.speed%10)  
		left_lane_col = self.col - 1
		right_lane_col = self.col + 1
		
		# Checking if the right and left lanes are in bound
		# and if they are, is it a lane that could be changed into
		left_lane_in_bound = self._lane_in_bound(left_lane_col)  # true or false
		valid_left_lane = left_lane_in_bound and self._can_change_into(freeway, self.row + 1, left_lane_col)

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
					if (freeway[self.row + i, left_lane_col, self.CAR_INDEX] == None and \
						freeway[self.row + i, left_lane_col, self.TIME_INDEX] < sim_time): 
						left_availability += 1

				# right lane
				if (valid_right_lane):
					if (freeway[self.row + i, right_lane_col, self.CAR_INDEX] == None and \
						freeway[self.row + i, right_lane_col, self.TIME_INDEX] < sim_time): 
						right_availability += 1

		# it's giving preference for right lane... like real life ;)
		# it might not get into this if elif if block at all 
		# if that happens, the car will just keep driving moving forward
		# TODO: 3+ REGULAR LANE CHANGING
		
		if (left_availability == space_needed):
			potential_space_switch_row = self.row + space_needed
			potential_space_switch_col = left_lane_col
		elif (right_availability == space_needed):
			potential_space_switch_row = self.row + space_needed
			potential_space_switch_col = right_lane_col
		# elif(right_availability == left_availability): # else they're equal or something
		# 	rand_num = np_rand.uniform(0.0, 1.0)
		# 	if (rand_num <= .5):
		# 		potential_space_switch_row = self.row + space_needed
		# 		potential_space_switch_col = right_lane_col
		# 	else:
		# 		potential_space_switch_row = self.row + space_needed
		# 		potential_space_switch_col = left_lane_col
		else: 
			self.move_forward(freeway, sim_time)
			return None # is this okay? Could I just have a return nothing

		#***************************************8
		index_to_check = freeway[potential_space_switch_row, potential_space_switch_col]
		# Check if it's a regular lane
		if (index_to_check[self.LANE_TYPE_INDEX] == self.REGULAR):
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
		function for regular lane cars that are next to the toll lane and
		it may or may not want to get into it (by chance)
		- If it does not meet the chance, it'll continue MOVE FORWARD
		- If it does meet, it'll switch into and speed is incremented
		
		Assumption: 
			- This car is already next to a toll lane that's at a section where you can change into
			and out of (the dotted line, not double lined)
	'''
	def change_into_toll(self, freeway, sim_time):
		pot_row = self.row + self.speed
		pot_col = self.col + 1
		count = 0
		# checking if there's enough room to get into the toll lane
		for i in range(1, self.speed + 1): 
			if (freeway[self.row + i, pot_col, self.CAR_INDEX] == None and \
				freeway[self.row + i, pot_col, self.TIME_INDEX] < sim_time):
				count += 1
		# if yes
		if (count == self.speed):
			rand_num = np_rand.uniform(0.0, 1.0)
			# by chance, it might move into it 
			if (rand_num <= self.PERC_CHANGE_TOLL):
				self._move_to_new(freeway, pot_row, pot_col, sim_time)
				if (self.speed < self.MAX_SPEED): 
						self.speed += 1
						return
		# IF all else above failed, just keep moving forward
		self.move_forward(freeway, sim_time)

	'''

		Assumption: 
			- The car is already in a toll lane that's rightest (which means it's near the regular lane)
				---> this means it's in the left lane if you're talking bout our grid cuz the grid is upside down
			- The car is at a section where it could change lane
			- this car wants to change out because it already met the percentage
				---> if it can't find a space at where it wants to go, it'll go to the last open space
		
		PROBLEMS:
			- [FIXED] this is trash currently, the switching out part is incorrect
	'''
	def toll_car_change_out(self, freeway, sim_time):
		pot_col = self.col - 1  # -1 because the lane it's checking is to its left on the grid
		open_space = 0
		for i in range(1, self.speed + 1):
			if (freeway[self.row + i, pot_col, self.CAR_INDEX] == None and \
				freeway[self.row +i, pot_col, self.TIME_INDEX] < sim_time):
				open_space += 1
			# it there is a car, stop incrementing open_spaces
			else: 
				break
		if (open_space > 0):
			pot_row = self.row + open_space
			self._move_to_new(freeway, pot_row, pot_col, sim_time)
		else:
			self.move_forward(freeway, sim_time)

	'''
		For cars that are in the toll lane and want to change lane internally
		---> actually i don't think i need this
		
		TODO: i can just call the change lane function i think
	'''
	def toll_car_change_lane(self, freeway, sim_time):
		pass

	'''
		Function for car on the freeway next to an on ramp
		to slow down for the car on the on ramp to be able to get
		on to the freeway
		If it didn't pass anything, it'll just MOVE FORWARD

		Parameter:
			freeway - the 3d array that represents the freeway and its values

		Assumption:
			The car is currently next to an on-ramp

		TODO:
			- this function does not yet take care of situations where there'd be 
			2+ on-ramp lanes that merges into one
			FIXME: I CAN'T GET THE speed of the car that was previously there!!! T_T
				FIX: i got rid of the time shit altogether in this function
	'''
	def next_to_ramp(self, freeway, sim_time):
		# ramps are to the left
		on_ramp_col = self.col - 1
		# CHECKING bigger than 0 just incase of some index mess up
		if (on_ramp_col >= 0):
			 
			space_to_check = freeway[self.row, on_ramp_col, self.CAR_INDEX] 
			# if there's a car next to it and it's at the same time stamp <--- TODO: is this even needed
			if (space_to_check != None):
				# if they're going at the same speed
				if (space_to_check.speed == self.speed):
					# there's a chance the car on the freeway will speed up
					rand_num = np_rand.uniform(0.0, 1.0)
					# SPEED UP
					if (rand_num <= self.PERC_SPEED_UP): 
						if (self.speed < self.MAX_SPEED):
							self.speed += 1
							self.move_forward(freeway, sim_time)
					# SLOW Down
					else:
						if (self.speed > self.MIN_SPEED):
							self.speed -= 1
							self.move_forward(freeway, sim_time)
		# all else failed keep moving forward
		self.move_forward(freeway, sim_time)

	'''
		Function for cars that are at the end of the ramp
		and want to merge onto the freeway
		It'll force itself in, even if it gotta slow down, 
		if it really really can't, it'll keep moving down the ramp or be stuck..
		which the move_forward function should take care of

		Parameter: 
			freeway - the 3d array that represents the freeway and its values
		
		Assumption:
			- this car is at a spot where it could merge onto the freeway
			- there's a lane to its right
		
		TODO::
			- i'm currently checking the time of the space i'm moving to
				do i care???
			- IF it can't merge to where it wants, find a space where it could (which means the car will slow down)
	'''
	def merge_onto_freeway(self, freeway, sim_time):
		# POT MEANS POTENTIAL, +1 because the freeway lane would be to right based on our
		# current configuration
		pot_col = self.col + 1
		open_space = 0
		for i in range(1, self.speed + 1):
			if (freeway[self.row + i, pot_col, self.CAR_INDEX] == None and \
				freeway[self.row +i, pot_col, self.TIME_INDEX] < sim_time):
				open_space += 1
			# it there is a car, stop incrementing open_spaces
			else: 
				break
		if (open_space > 0):
			pot_row = self.row + open_space
			self._move_to_new(freeway, pot_row, pot_col, sim_time)
		else: 
			self.move_forward(freeway, sim_time)

	'''
		TODO:i probably don't need this,
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
		
	# VERY BIG #TODO:
	# each freeway exit has a different percent that the driver will take it
	# each freeway exit has only once cell in which a car can exit, and once it has
	#     entered the exit ramp, it can not change its mind (will be forced to exit)
	# -- 30% for Bothell-Mill Creek (maybe exit 26)
	# -- 10% for all other
	'''
		Assumption:
		- this car is next to a spot where it can exit
		- the chance is already met for it to want to exit
	'''
	def exit_freeway(self, grid):

		# potential_space to exit <-- variable
		# generate random number and compare to exit percent
		# If randomly generated percentage is within the exit range
		#    take the exit and remove car from simulation after it reaches the end of the ramp
		# Else
		#    Do not take the exit and continue to move forward if there is room
		pass

	# TODO:: this function should just check for next available location
	# based on the car's current speed, don't check the whole thing??
	def _get_next_available_location(self, grid, sim_time):
		index_free = 0
		# Loop from one in front to 6 in front
		for i in range(1, 7): 
			row_to_check = self.row + i
			grid_to_check = grid[row_to_check, self.col]
			# FIXME: shouldn't the checking time be less than, not NOT EQUAL to
			if row_to_check < self.LAST_INDEX and\
			   sim_time != grid_to_check[self.TIME_INDEX] and\
			   grid_to_check[self.CAR_INDEX] == None and\
			   grid_to_check[self.LANE_TYPE_INDEX] != -1:

				index_free = index_free + 1
			else:
				break
		return index_free

	# This method will attempt to move the vehicle forward
	'''
		NICK GIVE SOME DESCRIPTION
		TODO:: 
			- not taking care of the case where the car might move onto a -1 lane type space
				-->> these are for on ramp situations 
			- slowing down thing?? car's looking ahead so it could slow down??
			   and not do the jump to the end of a car in a single second
	'''
	def move_forward(self, grid, sim_time):
		# TODO: NO NEED???
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