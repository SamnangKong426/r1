#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from serialarduino import ComArduino
import threading as th
import time

class VelocityTransformer(Node):
    def __init__(self):
        super().__init__('velocity_transformer')
        # self.publisher_ = self.create_publisher(Twist, 'transformed_cmd_vel', 10)
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.data = {
                #For Contol Velocity
                "Cmd_vel": [0, 0, 0]     
            }
        self.serial_arduino = ComArduino()
        th.Thread(target=self.serial_arduino.ar_read_from_port).start()
        time.sleep(1)

    def listener_callback(self, msg):
        print("Listener Callback")
        # Transform the incoming Twist message here if necessary
        self.data["Position"] = [msg.linear.x, msg.linear.y, msg.angular.z]
        self.serial_arduino.arser.write(str(self.data).encode())
        self.get_logger().info('I heard: "%s"' % str(self.data))
        time.sleep(0.3)
        
def main(args=None):
    rclpy.init(args=args)
    velocity_transformer = VelocityTransformer()
    rclpy.spin(velocity_transformer)
    velocity_transformer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()