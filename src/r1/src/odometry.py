#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
from geometry_msgs.msg import Point, Twist, PoseStamped
import math as m

class OdometryNode(Node):
    def __init__(self):
        super().__init__('odometryNode')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        # self.publisher_w = self.create_publisher(Float32, '/cmd_vel_w', 10)
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
        self.Ix = 0
        self.Iy = 0
        self.Iw = 0
        self.run_pos = False
        self.pos_msg = Point()
        self.poseStamped_msg = PoseStamped()

    def listener_callback(self, msg: PoseStamped):
        # self.get_logger().info('I heard: "%s"' % str(msg))
        self.poseStamped_msg = msg
        if self.run_pos:
            vx, vy, w = self.set_location(self.pos_msg.x, self.pos_msg.y, self.pos_msg.z)
            twist = Twist()
            twist.linear.x = vx
            twist.linear.y = vy
            twist.angular.z = w
            self.publisher.publish(twist)

    def locate_cmd_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % str(msg))
        self.pos_msg = msg
        self.run_pos = True

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
        position = self.poseStamped_msg.pose.position
        orientation = self.poseStamped_msg.pose.orientation
        # covert m to mm
        pos_x = position.z * 1000
        pos_z = position.x * 1000
        _, _, yaw = self.quaternion_to_rpy(orientation.x, orientation.y, orientation.z, orientation.w)
        # print("Roll: {}, Pitch: {}, Yaw: {}".format(roll, pitch, yaw))
        dx = self.pos_msg.x - pos_x
        dy = self.pos_msg.y - pos_z
        dw = self.pos_msg.z - yaw
        # Calculate distances to target
        d = self.distance(0, 0, dx, dy)
        # If the robot is close enough to the target, stop moving
        if abs(d) < 10 and abs(dw) < 2:
            self.Ix = self.Iy = self.Iw = 0
            print("Stop")
            self.run_pos = False
            return 0.0, 0.0, 0.0
        # Calculate velocities based on distances to target

        Px = dx * 0.5
        self.Ix = (self.Ix + dx) * 0.2
        Py = dy * 0.5
        self.Iy = (self.Iy + dy) * 0.2
        Pw = dw * 0.1
        self.Iw = (self.Iw + dw) * 0.1
        vx = Px+ self.Ix
        vy = Py+ self.Iy
        w = Pw + self.Iw
        vx = min(vx,800)
        vx = max(vx,-800)
        vy = min(vy,800)
        vy = max(vy,-800)
        w = min(w, 45)
        w = max(w, -45)

        # w_msg = Float32()
        # w_msg.data = yaw
        # self.publisher_w.publish(w_msg)

        vx, vy = self.next_vel(vx, vy, yaw)
        # self.get_logger().info('Velocity : %s, %s, %s' % (vx, vy, w))
        return float(vx), float(vy), float(w)
    
    # def set_locationv1(self, x, y, w):
    #     position = self.poseStamped_msg.pose.position
    #     orientation = self.poseStamped_msg.pose.orientation
    #     # covert m to mm
    #     pos_x = position.z * 1000
    #     pos_z = position.x * 1000

    #     _, _, yaw = self.quaternion_to_rpy(orientation.x, orientation.y, orientation.z, orientation.w)
    #     # print("Roll: {}, Pitch: {}, Yaw: {}".format(roll, pitch, yaw))
    #     dx = self.pos_msg.x - pos_x
    #     dy = self.pos_msg.y - pos_z
    #     dw = self.pos_msg.z - yaw

    #     d = self.distance(0, 0, dx, dy)
    #     if abs(d) < 10 and abs(dw) < 2:
    #         print("Stop")
    #         self.run_pos = False
    #         return 0.0, 0.0, 0.0

    #     vx = dx * 0.5
    #     vy = dy * 0.5 
    #     w = dw * 0.04 
    #     return vx, vy, w
        

def main(args=None):
    rclpy.init(args=args)
    odometry_node = OdometryNode()
    rclpy.spin(odometry_node)
    odometry_node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()