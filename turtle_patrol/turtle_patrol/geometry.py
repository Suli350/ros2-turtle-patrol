"""Small, ROS-free geometry helpers so they can be unit tested with plain pytest."""
import math


def normalize_angle(angle):
    """Wrap an angle to the range [-pi, pi)."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)


def pairs(flat):
    """Turn [x1, y1, x2, y2, ...] into [(x1, y1), (x2, y2), ...]."""
    if len(flat) < 2 or len(flat) % 2 != 0:
        raise ValueError('waypoints must be a non-empty list of x, y pairs')
    return list(zip(flat[0::2], flat[1::2]))
