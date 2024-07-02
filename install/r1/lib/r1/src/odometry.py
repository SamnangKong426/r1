#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped, Twist
import math as m
import json

class PoseSubscriber(Node):
    def __init__(self):
        super().__init__('pose_subscriber')
        self.publisher = self.create_publisher(Twist, '/r1/cmd_vel', 10)
        self.subscription = self.create_subscription(
            PoseStamped,
            '/camera/pose/sample',
            self.listener_callback,
            10
        )
        
        self.arduino_sub = self.create_subscription(
            String,
            '/arduinoController',
            self.arduinoListener_callback,
            10
        )
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        twist = Twist()
        twist.linear.x = msg.pose.position.x
        twist.linear.y = msg.pose.position.y
        twist.angular.z = msg.pose.position.z
        roll, pitch, yaw = self.quaternion_to_rpy(msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w)
        self.publisher.publish(twist)
        # self.get_logger().info('I published: "%s"' % twist)
        # self.get_logger().info('I heard: "%s"' % msg)
    
    def arduinoListener_callback(self, msg):
        try:
            data = json.loads(msg.data)
            print(data)
        except:
            print("Error loading JSON")

    def quaternion_to_rpy(self, rs_x, rs_y, rs_z, rs_w):
        w = rs_w
        x = -rs_z
        y = rs_x
        z = -rs_y

        pitch =  -m.asin(2.0 * (x*z - w*y)) * 180.0 / m.pi
        roll  =  m.atan2(2.0 * (w*x + y*z), w*w - x*x - y*y + z*z) * 180.0 / m.pi
        yaw   =  -m.atan2(2.0 * (w*z + x*y), w*w + x*x - y*y - z*z) * 180.0 / m.pi
        print("RPY [deg]: Roll: {0:.7f}, Pitch: {1:.7f}, Yaw: {2:.7f}".format(roll, pitch, yaw))
        return roll, pitch, yaw

def main(args=None):
    rclpy.init(args=args)
    pose_subscriber = PoseSubscriber()
    rclpy.spin(pose_subscriber)
    pose_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()