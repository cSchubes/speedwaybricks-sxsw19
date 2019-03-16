import LowPassFilter
import rover_lib

class GradientDescent:
    def __init__(self, lowpass_coeff, step_size):
        self.signal_filter = LowPassFilter(lowpass_coeff)
        self.prev_signal = 0
        self.this_signal = 0
        self.step = step_size
        self.prev_pos = 0

        self.enter_deadzone()

    def enter_deadzone():
        return

    def get_next_step(self, new_robot_pos, new_signal):
        return
