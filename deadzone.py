import LowPassFilter
from rover_lib import *
import numpy

class GradientDescent:

    prev_pos = robot_state(poser(0,0,0,0,0,0))
    
    def __init__(self, first_signal, first_state, params):
        # Call with deadzone_params, set in parameters.py file
        self.alpha = params[0]
        self.max_turn = params[3]
        self.beta = params[1]
        self.gamma = params[2]

        self.prev_signal = first_signal
        self.this_signal = first_signal
        self.prev_heading = first_state.heading
        self.goal_heading = first_state.heading

        self.signal_filter = LowPassFilter(params[4])
        self.heading_filter = LowPassFilter(params[5])

        self.signal_filter.reset(first_signal)
        self.heading_filter.reset(first_state.heading)

        self.starting_counter = 0

    def get_next_step(self, new_robot_pos, new_signal):

        new_signal = self.signal_filter.filter(new_signal)
        new_heading = self.heading_filter.filter(new_robot_pos.heading)

        if(self.starting_counter < 3):
            self.starting_counter += 1
            self.prev_signal = new_signal
            self.prev_heading = new_heading
            return goal_heading
        
        ds = new_signal - self.prev_signal
        dh = new_heading - self.prev_heading

        heading_step = numpy.sign(ds) * self.max_turn * abs((self.beta - ds)/(self.beta - self.alpha)) * self.gamma * abs(dh)
        goal_heading += heading_step

        self.prev_signal = new_signal
        self.prev_heading = new_heading

        return goal_heading

