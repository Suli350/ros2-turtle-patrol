"""Integrate the turtle's travelled distance and publish it once per second."""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from turtlesim.msg import Pose

from turtle_patrol.geometry import distance


class OdometerNode(Node):

    def __init__(self):
        super().__init__('odometer_node')
        self.total = 0.0
        self.last = None
        self.pub = self.create_publisher(Float64, 'distance_traveled', 10)
        self.create_subscription(Pose, 'turtle1/pose', self.on_pose, 10)
        self.create_timer(1.0, self.publish_total)

    def on_pose(self, msg):
        if self.last is not None:
            self.total += distance(self.last.x, self.last.y, msg.x, msg.y)
        self.last = msg

    def publish_total(self):
        self.pub.publish(Float64(data=self.total))
        self.get_logger().debug(f'distance traveled: {self.total:.2f} m')


def main(args=None):
    rclpy.init(args=args)
    node = OdometerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
