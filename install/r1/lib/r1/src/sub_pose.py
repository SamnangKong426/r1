#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry

class CameraPoseSubscriber(Node):
    def __init__(self):
        super().__init__('camera_pose_subscriber')
        self.subscription = self.create_subscription(
            Odometry,
            '/camera/pose/sample',
            self.listener_callback,
            200)
        self.subscription  # prevent unused variable warning
        print("Subscribed to /camera/pose/sample")

    def listener_callback(self, msg):
        position = msg.pose.pose.position
        print(f"Received pose: Position = x: {position.x}, y: {position.y}, z: {position.z}")

def main(args=None):
    rclpy.init(args=args)
    camera_pose_subscriber = CameraPoseSubscriber()
    rclpy.spin(camera_pose_subscriber)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    camera_pose_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()