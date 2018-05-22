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
	def _closest_car_in_front_speed(self, grid, row, col): 
		pass
        # search for the nearest car 

	# changing lane is moving diagionally  
	def change_lane(self):
        # potential_space _switch < --- variable
        # left_speed = 0
        # right_speed = 0
        # Check if there's an open space next to you (left and right)
			# diagonal space <--- sooooo left = i[self.row + 1][self.col +1 or -1][tuple car object] == None
        #### checking which lane is faster
        # if (left space exists)
            # left_speed = _closest_car_in_front_speed(grid, row_of_left_space, col_of_left_space)
        # if (right space exists)
            # right_speed = _closest_car_in_front_speed(grid, row_of_right_space, col_of_right_space)
        # potential_space_switch = whichever speed is bigger (right_speed vs left_left)

		pass