#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point, Twist, PoseStamped
import math as m
import json

class OdometryNode(Node):
    def __init__(self):
        super().__init__('odometryNode')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            PoseStamped,
            '/camera/pose/sample',
            self.listener_callback,
            10
        )
        self.cmd_sub = self.create_subscription(
            Point,
            '/position',
            self.locate_cmd_callback,
            10
        )
        # robot location
        self.pos_msg = PoseStamped()
    def listener_callback(self, msg: PoseStamped):
        self.get_logger().info('I heard: "%s"' % str(msg))

    def locate_cmd_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % str(msg))

def main(args=None):
    rclpy.init(args=args)
    odometry_node = OdometryNode()
    rclpy.spin(odometry_node)
    odometry_node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()