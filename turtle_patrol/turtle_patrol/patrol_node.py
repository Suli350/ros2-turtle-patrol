"""Drive turtle1 around a list of waypoints forever.

Concepts: publisher, subscriber, timer, parameters (re-read every cycle so
`ros2 param set` works live) and a service server.
"""
import math

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_srvs.srv import Trigger
from turtlesim.msg import Pose

from turtle_patrol.geometry import distance, normalize_angle, pairs


class PatrolNode(Node):

    def __init__(self):
        super().__init__('patrol_node')
        self.declare_parameter('waypoints', [2.0, 2.0, 9.0, 2.0, 9.0, 9.0, 2.0, 9.0])
        self.declare_parameter('linear_speed', 1.5)
        self.declare_parameter('angular_gain', 4.0)
        self.declare_parameter('goal_tolerance', 0.15)
        self.declare_parameter('control_rate', 20.0)

        self.waypoints = pairs(list(self.get_parameter('waypoints').value))
        self.index = 0
        self.laps = 0
        self.pose = None

        self.cmd_pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.create_subscription(Pose, 'turtle1/pose', self.on_pose, 10)
        self.create_service(Trigger, 'reset_patrol', self.on_reset)

        rate = self.get_parameter('control_rate').value
        self.create_timer(1.0 / rate, self.control_loop)
        self.get_logger().info(f'Patrolling {len(self.waypoints)} waypoints: {self.waypoints}')

    def on_pose(self, msg):
        self.pose = msg

    def on_reset(self, request, response):
        self.index = 0
        self.laps = 0
        response.success = True
        response.message = 'Patrol reset to first waypoint'
        self.get_logger().info(response.message)
        return response

    def control_loop(self):
        if self.pose is None:
            return
        speed = self.get_parameter('linear_speed').value
        gain = self.get_parameter('angular_gain').value
        tolerance = self.get_parameter('goal_tolerance').value

        gx, gy = self.waypoints[self.index]
        dist = distance(self.pose.x, self.pose.y, gx, gy)

        if dist < tolerance:
            self.index = (self.index + 1) % len(self.waypoints)
            if self.index == 0:
                self.laps += 1
                self.get_logger().info(f'Lap {self.laps} complete')
            else:
                self.get_logger().info(f'Reached waypoint, heading to #{self.index}')
            return

        heading_error = normalize_angle(
            math.atan2(gy - self.pose.y, gx - self.pose.x) - self.pose.theta)

        cmd = Twist()
        cmd.angular.z = gain * heading_error
        # Only move forward when roughly facing the goal; slow down near it.
        cmd.linear.x = min(speed, 1.5 * dist) * max(0.0, math.cos(heading_error)) ** 2
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
