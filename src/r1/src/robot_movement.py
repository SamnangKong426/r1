#!/usr/bin/env python3
import serial
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from serialarduino import ComArduino
import threading as th
import time

class VelocityTransformer(Node):
    def __init__(self):
        super().__init__('velocity_transformer')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            1)
        self.data = {
                #For Contol Velocity
                "Cmd_vel": [0, 0, 0]     
            }
        self.serial_arduino = ComArduino()
        th.Thread(target=self.serial_arduino.ar_read_from_port).start()

    def listener_callback(self, msg):
        def listener_callback(self, msg):
            self.data["Cmd_vel"] = [msg.linear.x, msg.linear.y, msg.angular.z]
            # try:
                # Ensure the serial buffer is clear before writing
            self.serial_arduino.arser.reset_output_buffer()
            self.serial_arduino.arser.write(str(self.data).encode())
            # except serial.SerialTimeoutException as e:
            #     self.get_logger().error(f'Write timeout occurred: {e}')
            #     # Handle the timeout, e.g., by retrying or logging
            # else:
            #     self.get_logger().info('I heard: "%s"' % str(self.data))
        
def main(args=None):
    rclpy.init(args=args)
    velocity_transformer = VelocityTransformer()
    rclpy.spin(velocity_transformer)
    velocity_transformer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()