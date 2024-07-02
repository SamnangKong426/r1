import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart

from launch_ros.actions import Node



def generate_launch_description():

    package_name = "r1"

    camera_t265 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("realsense2_camera"), 'launch', 'rs_launch.py')
        )
    )

    odometry_node = Node(
        package='r1',
        executable='odometry.py',
        name='odometry',
        output='screen',
    )

    return LaunchDescription([
        camera_t265,
        odometry_node,
    ])