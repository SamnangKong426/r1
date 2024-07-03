#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from std_msgs.msg import Float32
from geometry_msgs.msg import PoseStamped
import pyrealsense2 as rs
import math as m
from scipy.spatial.transform import Rotation as R


class T265Publisher(Node):

    def __init__(self):
        super().__init__('camera_t265')
        self.publisher_imu = self.create_publisher(Imu, 'camera/imu_data', 10)
        self.publisher_pose = self.create_publisher(PoseStamped, 'camera/pose/sample', 10)
        self.publisher_picth = self.create_publisher(Float32, 'camera/pitch', 10)
        self.publisher_picthKalman = self.create_publisher(Float32, 'camera/picthKalman', 10)
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
            # if data.tracker_confidence != 3:
            #     print("conf: {}".format(data.tracker_confidence))
                
            # elif data.tracker_confidence == 3 and self.first: 
            #     print("confidence: 3")
            #     self.first = False
            
            roll, picth , yaw = self.quaternion_to_rpy(data.rotation.x, data.rotation.y, data.rotation.z, data.rotation.w)
            # print("roll: {}, pitch: {}, yaw: {}".format(roll, picth, yaw))
            
            pitch_msg = Float32()
            pitch_msg.data = picth
            self.publisher_picth.publish(pitch_msg)

            self.kf.predict()
            self.kf.update(pitch)
            pitch = self.kf.state
            
            pitchKalman_msg = Float32()
            pitchKalman_msg.data = pitch
            self.publisher_picthKalman.publish(pitchKalman_msg)
        
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

    def quaternion_to_rpy(self, x, y, z, w):
        r = R.from_quat([x, y, z, w])
        roll, pitch, yaw = r.as_euler('xyz', degrees=True)
        return roll, pitch, yaw

    # def quaternion_to_rpy(self, rs_x, rs_y, rs_z, rs_w):
    #     w = rs_w
    #     x = -rs_z
    #     y = -rs_x
    #     z = rs_y

    #     pitch =  -m.asin(2.0 * (x*z - w*y)) * 180.0 / m.pi
    #     roll  =  m.atan2(2.0 * (w*x + y*z), w*w - x*x - y*y + z*z) * 180.0 / m.pi
    #     yaw   =  m.atan2(2.0 * (w*z + x*y), w*w + x*x - y*y - z*z) * 180.0 / m.pi
    #     # print("RPY [deg]: Roll: {0:.7f}, Pitch: {1:.7f}, Yaw: {2:.7f}".format(roll, pitch, yaw))
    #     return roll, pitch, yaw

def main(args=None):
    rclpy.init(args=args)
    t265_publisher = T265Publisher()
    rclpy.spin(t265_publisher)
    t265_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
