import numpy as np

class KalmanFilter:

    def __init__(self, process_noise, measurement_noise, estimated_error, initial_value=0):
        # Process noise variance (Q)
        self.process_noise = process_noise
        # Measurement noise variance (R)
        self.measurement_noise = measurement_noise
        # Estimated error in initial state (P)
        self.estimated_error = estimated_error
        # Initial value of the state (x)
        self.state = initial_value

    def predict(self):
        # Predict the next state
        # In this simple example, we assume a direct transfer, so no specific action is taken
        self.estimated_error += self.process_noise

    def update(self, measurement):
        # Kalman Gain (K)
        kalman_gain = self.estimated_error / (self.estimated_error + self.measurement_noise)
        # Update state with measurement and Kalman Gain
        self.state = self.state + kalman_gain * (measurement - self.state)
        # Update the error covariance
        self.estimated_error = (1 - kalman_gain) * self.estimated_error

# Example usage
# kf = KalmanFilter(process_noise=1e-5, measurement_noise=1e-2, estimated_error=1e-2)
# measurements = [1, 2, 3, 2, 1]  # Example measurements

# for measurement in measurements:
#     kf.predict()
#     kf.update(measurement)
#     print(f"Updated state: {kf.state}")