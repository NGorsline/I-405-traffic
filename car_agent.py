class Car:
   # Constructor 
	def __init__(self, x, y):
		# class variables
		self.curr_location = (x, y)
        self.completed = False
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