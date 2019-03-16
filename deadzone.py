import LowPassFilter
from rover_lib import *
import numpy

class GradientDescent:

    prev_pos = robot_state(poser(0,0,0,0,0,0))
    
    def __init__(self, alpha, beta, max_turn, gamma, first_signal, first_state, lowpass_signal_coeff, lowpass_heading_coeff):
        self.alpha = alpha
        self.max_turn = max_turn
        self.beta = beta
        self.gamma = gamma

        self.prev_signal = first_signal
        self.this_signal = first_signal
        self.prev_heading = first_state.heading
        self.goal_heading = first_state.heading

        self.signal_filter = LowPassFilter(lowpass_signal_coeff)
        self.heading_filter = LowPassFilter(lowpass_heading_coeff)

        self.starting_counter = 0

    def get_next_step(self, new_robot_pos, new_signal):

        if(self.starting_counter < 3):
            self.starting_counter += 1
            return goal_heading
        
        new_signal = self.signal_filter.filter(new_signal)
        new_heading = self.heading_filter.filter(new_robot_pos.heading)
        
        ds = new_signal - self.prev_signal
        dh = new_heading - self.prev_heading

        heading_step = numpy.sign(ds) * self.max_turn * abs((self.beta - ds)/(self.beta - self.alpha)) * self.gamma * abs(dh)
        goal_heading += heading_step

        self.prev_signal = new_signal
        self.prev_heading = new_heading

        return goal_heading

