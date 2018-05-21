# THEM CARS MOVING AND SHIT
a = 3
print ("man wtf" + str(a))
#fuck you

class Car:
    # Constructor 
    def __init__(self, x, y):
        # class variables
        self.curr_location = (x, y)
        self.finishing_time = None  # will be set when car passes the end of the road

    def switch_lane(self):
        # some shit
        return 1

    
    def drive(self):
        # change lane 
        # move foward (accelerate and decelerate accordingly)
        # enter toll lane if near it (by a percent)
        # exit if near exit (by a percent)
        # stay 
        return 1


    def closest_car_in_front_speed(self, grid, row, col): 
        pass
        # return the speed of the car in front of the row and col
    
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
    
    
    def merge(self):
        pass  # PASS FOR NOW CUZ WE NEED A BODY

    def enter_toll_lane(self):
        pass
    

    


    
