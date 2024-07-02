import rclpy  # Import ROS2 python library
from rclpy.node import Node  # Import Node module
from std_msgs.msg import String  # Import String message type from standard messages

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')  # Initialize the Node with the name 'simple_publisher'
        self.publisher_ = self.create_publisher(String, 'chatter', 10)  # Create a publisher on the 'chatter' topic
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)  # Create a timer to call the callback every 0.5 seconds

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello ROS2 Foxy'  # Message to be published
        self.publisher_.publish(msg)  # Publish the message
        self.get_logger().info('Publishing: "%s"' % msg.data)  # Log the published message

def main(args=None):
    rclpy.init(args=args)  # Initialize ROS2 communication
    simple_publisher = SimplePublisher()  # Create the publisher object
    rclpy.spin(simple_publisher)  # Keep the node alive to continue publishing messages

    simple_publisher.destroy_node()  # Cleanup the node
    rclpy.shutdown()  # Shutdown ROS2 communication

if __name__ == '__main__':
    main()