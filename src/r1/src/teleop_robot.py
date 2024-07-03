#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point

class PositionPublisher(Node):

    def __init__(self):
        super().__init__('position_publisher')
        self.publisher_ = self.create_publisher(Point, 'position', 10)
        self.timer_period = 0.01
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

    def timer_callback(self):
        x = float(input("Enter the x coordinate: "))
        y = float(input("Enter the y coordinate: "))
        z = float(input("Enter the z coordinate: "))

        msg = Point()
        msg.x = x
        msg.y = y
        msg.z = z

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%f %f %f"' % (msg.x, msg.y, msg.z))


def main(args=None):
    rclpy.init(args=args)
    position_publisher = PositionPublisher()
    rclpy.spin(position_publisher)
    position_publisher.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()