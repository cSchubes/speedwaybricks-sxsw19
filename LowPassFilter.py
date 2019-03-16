class LowPassFilter:
    def __init__(self, coeff):
        self.prev_msrmts_ = [0, 0, 0]
        self.prev_filtered_msrmts_ = [0, 0]
        self.filter_coeff_ = coeff

    def reset(self, value):
        prev_msrmts_ = [value, value, value]
        prev_filtered_msrmts_ = [value, value]

    def filter(self, new_msrmt):
        # Push in the new measurement
        self.prev_msrmts_[2] = self.prev_msrmts_[1];
        self.prev_msrmts_[1] = self.prev_msrmts_[0];
        self.prev_msrmts_[0] = new_msrmt;

        new_filtered_msrmt = (1 / (1 + self.filter_coeff_ * self.filter_coeff_ + 1.414 * self.filter_coeff_)) * \
        (self.prev_msrmts_[2] + 2 * self.prev_msrmts_[1] + self.prev_msrmts_[0] - (self.filter_coeff_ * \
        self.filter_coeff_ - 1.414 * self.filter_coeff_ + 1) * self.prev_filtered_msrmts_[1] - \
        (-2 * self.filter_coeff_ * self.filter_coeff_ + 2) * self.prev_filtered_msrmts_[0]);

        # Store the new filtered measurement
        self.prev_filtered_msrmts_[1] = self.prev_filtered_msrmts_[0];
        self.prev_filtered_msrmts_[0] = new_filtered_msrmt;

        return new_filtered_msrmt;
