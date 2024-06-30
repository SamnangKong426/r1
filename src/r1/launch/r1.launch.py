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

    # camera = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(get_package_share_directory(package_name), 'launch', 'camera.launch.py')
    #     )
    # )

    # camera_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         os.path.join(get_package_share_directory('realsense2_camera'), 'launch', 'rs_launch.py')
    #     )
    # )

    camera_node = Node(
        package='r1',
        executable='camera_node.py',
        name='camera_node',
        output='screen',
    )

    odometry_node = Node(
        package='r1',
        executable='odometry.py',
        name='odometry',
        output='screen',
    )



    return LaunchDescription([
        camera_node,
        odometry_node,
    ])