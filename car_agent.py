class Car:
   # Constructor 
	def __init__(self, row, col):
		# class variables
		self.speed = None # will be set when the car is created
		self.curr_location = (row, col) # location that the vehicle is currently at
		self.completed = False # If the car has left the simulation
		self.starting_time = None  # will be set when car is spawned into the sim
		self.finishing_time = None  # will be set when car passes the end of the road

	def drive(self):
       # change lane   <-- TRAN
       # move foward (accelerate and decelerate accordingly)
       # enter toll lane if near it (by a percent)
       # exit if near exit (by a percent)
       # stay 
		pass


    # TRAN'S SECTION#########################################################3
	# helper function for change_lane
	def closest_car_in_front_speed(self, grid, row, col): 
		pass
        # search for the nearest car 

	def change_lane(self):
        # potential_space _switch < --- variable
        # left_speed = 0
        # right_speed = 0
        # Check if there's an open space next to you (left and right) 
        #### checking which lane is faster
        # if (left space exists)
            # left_speed = closest_car_in_front_speed(grid, row_of_left_space, col_of_left_space)
        # if (right space exists)
            # closest_car_in_front_speed(grid, row_of_right_space, col_of_right_space)
        # potential_space_switch = 
		pass
	
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

