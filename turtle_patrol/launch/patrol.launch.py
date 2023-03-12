import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    params = os.path.join(get_package_share_directory('turtle_patrol'), 'config', 'patrol.yaml')
    return LaunchDescription([
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        Node(package='turtle_patrol', executable='patrol_node', parameters=[params], output='screen'),
        Node(package='turtle_patrol', executable='odometer_node', output='screen'),
    ])
