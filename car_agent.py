class Car:
	MAX_SPEED = 6
	SPEED_PER = 10.22 # mph per speed step
	CAR = 2  # the index which holds the car value
	TIME = 1
   # Constructor 
	def __init__(self, row, col):
		# class variables
		self.speed = 0  # TEMP SET TO 0 # will be set when the car is created
		self.row = row # location that the vehicle is currently at
		self.col = col # location that the vehicle is currently at
		self.completed = False # If the car has left the simulation
		self.starting_time = None  # will be set when car is spawned into the sim
		self.finishing_time = None  # will be set when car passes the end of the road

	def _set_location(self, row, col):
		self.curr_row = row
		self.curr_col = col

	def drive(self, grid):
	   # change lane   <-- TRAN
	   # move foward (accelerate and decelerate accordingly)
	   self.move_forward(grid)
	   # enter toll lane if near it (by a percent)
	   # exit if near exit (by a percent)
	   # stay 


	# TRAN'S SECTION#########################################################3
	# helper function for change_lane
	def _closest_car_in_front(self, freeway, row, col):
		# search for the nearest car
		space_needed = (self.speed%10) - 1
		index_away = 1
		car_speed = 60.0

		for i in range(6 - space_needed): 
			if (freeway[row + i, col, self.CAR] != None):
				return freeway[row + i, col, self.CAR].speed
		return car_speed
		
				

	# changing lane is moving diagionally  
	def change_lane(self, freeway):
		# potential_space _switch < --- variable
		left_speed = 0.0  # mph
		right_speed = 0.0 # mph
		space_needed = (self.speed%10) - 1  # space travel within a second based on currently speed
		# Check if there's an open space next to you (left and right)
		#### checking which lane is faster
		if (freeway[self.row + space_needed, self.col -1, self.CAR] != None):  # if left space exists
			left_speed = _closest_car_in_front_speed(freeway, self.row + space_needed, self.col - 1)
		if (freeway[self.row + space_needed, self.col +1, self.CAR] != None):  # if right space exists
			right_speed = _closest_car_in_front_speed(freeway, self.row + space_needed, self.col + 1)
		

		# apparently numbers can be compared to the value type 'None'
		if (left_speed > right_speed and left_speed > self.speed):
			potential_space_switch_row = self.row + space_needed
			potential_space_switch_col = self.col - 1
		elif (right_speed > left_speed and right_speed > self.speed):
			potential_space_switch_row = self.row + space_needed
			potential_space_switch_col = self.col + 1
		# potential_space_switch = whichever speed is bigger (right_speed vs left_left)
		# DON'T FORGET to ooo REMOVEEEE A CAR ONCE YOU'VE MOVED IT *****************************8
		
	
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

	# This method will attempt to move the vehicle forward
	def move_forward(self, grid):

		# Create helper function to check if the spaces in front will be clear at the speed traveled
		if self.speed == 0 and self.curr_row < 2319: ## SECOND AND IS TEMP
			new_row = self.curr_row + 1
			new_col = self.curr_col
			# Check to see if the proposed new spot has a car at that location
			if grid[new_row, new_col, 2] == None: # ADD AN AND TO CHECK IF THE CAR WAS JUST THERE
				# Create helper to move car from source location to target location
				grid[new_row, new_col, 2] = grid[self.curr_row, self.curr_col, 2]
				grid[self.curr_row, self.curr_col, 2] = None
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

