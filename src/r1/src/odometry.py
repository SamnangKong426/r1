#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point, Twist
from nav_msgs.msg import Odometry
import math as m
import json

class OdometryNode(Node):
    def __init__(self):
        super().__init__('odometryNode')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.subscription = self.create_subscription(
            Odometry,
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
        self.pos_msg = Odometry()

        # robot PID
        self.Ix = 0
        self.Iy = 0
        self.Iw = 0

        self.x = 500.0
        self.y = 0.0
        self.w = 0.0

    def listener_callback(self, msg: Odometry):
        self.get_logger().info('I heard: "%s"' % str(msg))
        self.pos_msg = msg
        vx, vy, w = self.set_location(self.x, self.y, self.w)
        twist = Twist()
        twist.linear.x = vx
        twist.linear.y = vy
        twist.angular.z = w
        self.publisher.publish(twist)
    
    def locate_cmd_callback(self, msg):
        self.x = msg.x  # next position x
        self.y = msg.y  # next position y
        self.w = msg.z  # next position w

    def quaternion_to_rpy(self, rs_x, rs_y, rs_z, rs_w):
        w = rs_w
        x = -rs_z
        y = rs_x
        z = -rs_y
        pitch =  -m.asin(2.0 * (x*z - w*y)) * 180.0 / m.pi
        roll  =  m.atan2(2.0 * (w*x + y*z), w*w - x*x - y*y + z*z) * 180.0 / m.pi
        yaw   =  -m.atan2(2.0 * (w*z + x*y), w*w + x*x - y*y - z*z) * 180.0 / m.pi
        # print("RPY [deg]: Roll: {0:.7f}, Pitch: {1:.7f}, Yaw: {2:.7f}".format(roll, pitch, yaw))
        return -roll, pitch, yaw
    
    def next_vel(self, vx, vy, yaw):
        next_vx = (vx * m.cos(m.radians(yaw))) + (vy * m.sin(m.radians(yaw)))
        next_vy = -(vx * m.sin(m.radians(yaw))) + (vy * m.cos(m.radians(yaw)))
        # print("Next_vx: {}, Next_vy: {}".format(next_vx, next_vy))
        return next_vx, next_vy
    
    def distance(self, x1, y1, x2, y2):
        return m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    def set_location(self, x, y, w):
        position = self.pos_msg.pose.pose.position
        orientation = self.pos_msg.pose.pose.orientation
        # covert m to mm
        pos_x = - position.x * 1000
        pos_z = - position.y * 1000
        roll, _, _ = self.quaternion_to_rpy(orientation.x, orientation.y, orientation.z, orientation.w)
        print("Position: {}, {}, {}".format(pos_x, pos_z, roll))
        dx = self.x - pos_z
        dy = self.y - pos_x  
        dw = self.w - roll
        # Calculate distances to target
        d = self.distance(0, 0, dx, dy)
        # If the robot is close enough to the target, stop moving
        if d < 10 and abs(dw) < 10:
            self.Ix = self.Iy = self.Iw = 0
            print("Stop")
            return 0.0, 0.0, 0.0
        # Calculate velocities based on distances to target
        vx = dx * 0.5
        vy = dy * 0.5
        w = dw * 0.005

        # vx = min(vx,500)
        # vx = max(vx,-500)
        # vy = min(vy,500)
        # vy = max(vy,-500)
        # w = min(w, 25)
        # w = max(w, -25)

        """Px = dx * 0.5
        self.Ix = (self.Ix + dx) * 0.2
        Py = dy * 0.5
        self.Iy = (self.Iy + dy) * 0.2
        Pw = dw * 0.005
        self.Iw = (self.Iw + dw) * 0.005
        vx = Px+ self.Ix
        vy = Py+ self.Iy
        w = Pw + self.Iw
        vx = min(vx,800)
        vx = max(vx,-800)
        vy = min(vy,800)
        vy = max(vy,-800)
        w = min(w, 45)
        w = max(w, -45)
        """
        # vx, vy = self.next_vel(vx, vy, roll)
        # self.get_logger().info('Velocity : %s, %s, %s' % (vx, vy, w))
        return float(vx), float(vy), float(w)

def main(args=None):
    rclpy.init(args=args)
    odometry_node = OdometryNode()
    rclpy.spin(odometry_node)
    odometry_node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()