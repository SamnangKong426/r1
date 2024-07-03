#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import PoseStamped
import pyrealsense2 as rs
import os

class T265Publisher(Node):

    def __init__(self):
        super().__init__('camera_t265')
        self.publisher_imu = self.create_publisher(Imu, 'camera/imu_data', 10)
        self.publisher_pose = self.create_publisher(PoseStamped, 'camera/pose/sample', 10)
        self.timer_period = 0.01  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # Configure the T265 camera
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.pose)
        self.pipeline.start(self.config)
        self.first = True

    def timer_callback(self):
        frames = self.pipeline.wait_for_frames()
        pose_frame = frames.get_pose_frame()
        if pose_frame:
            data = pose_frame.get_pose_data()
            # print("Frame #{}".format(pose_frame.frame_number))
            if data.tracker_confidence != 3:
                print("conf: {}".format(data.tracker_confidence))
            elif data.tracker_confidence == 3 and self.first: 
                print("conf: {}".format(data.tracker_confidence))
                self.first = False
        
            imu_msg = Imu()
            imu_msg.orientation.x = data.rotation.x
            imu_msg.orientation.y = data.rotation.y
            imu_msg.orientation.z = data.rotation.z
            imu_msg.orientation.w = data.rotation.w

            pose_msg = PoseStamped()
            pose_msg.pose.position.x = data.translation.x
            pose_msg.pose.position.y = data.translation.y
            pose_msg.pose.position.z = data.translation.z
            pose_msg.pose.orientation.x = data.rotation.x
            pose_msg.pose.orientation.y = data.rotation.y
            pose_msg.pose.orientation.z = data.rotation.z
            pose_msg.pose.orientation.w = data.rotation.w

            self.publisher_imu.publish(imu_msg)
            self.publisher_pose.publish(pose_msg)

def main(args=None):
    rclpy.init(args=args)
    t265_publisher = T265Publisher()
    rclpy.spin(t265_publisher)
    t265_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
