#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from serialarduino import SerialArduino
import threading as th
import time

class VelocityTransformer(Node):
    def __init__(self):
        super().__init__('odometry_transformer')
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(String, 'arduinoController', 10)
        self.timer_period = 0.01
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        self.data = {
            "cmd_vel": [0, 0, 0] # [linear.x, linear.y, angular.z]
        }
        self.serial_arduino = SerialArduino()
        th.Thread(target=self.serial_arduino.ar_read_from_port).start()

    def listener_callback(self, msg):
        self.data["cmd_vel"] = [msg.linear.x, msg.linear.y, msg.angular.z]
        self.serial_arduino.arser.write(str(self.data).encode())
        time.sleep(0.3)
        self.get_logger().info("I heard: '%s'" % str(self.data))


    def timer_callback(self):
        msg = String()
        msg.data = self.serial_arduino.msg
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    velocity_transformer = VelocityTransformer()
    rclpy.spin(velocity_transformer)
    velocity_transformer.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
