# ROS2 Turtle Patrol

A first ROS2 project: make `turtlesim` patrol a list of waypoints forever.

![stack](https://img.shields.io/badge/ROS2-Humble-blue) ![python](https://img.shields.io/badge/python-3.10-green)

## What you learn

| Concept | Where |
|---|---|
| Publisher / subscriber | `patrol_node.py` publishes `turtle1/cmd_vel`, subscribes `turtle1/pose` |
| Timers & control loops | 20 Hz proportional heading controller |
| Parameters (YAML + live changes) | `config/patrol.yaml`, `ros2 param set` |
| Service server | `/reset_patrol` (`std_srvs/Trigger`) |
| Launch files | `launch/patrol.launch.py` starts three nodes |
| Unit testing without ROS | `test/test_geometry.py` |

## Build

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/<you>/ros2-turtle-patrol.git
cd ~/ros2_ws
rosdep install --from-paths src -y --ignore-src
colcon build --symlink-install
source install/setup.bash
```

## Run

```bash
ros2 launch turtle_patrol patrol.launch.py
```

Things to try in a second terminal:

```bash
ros2 topic echo /distance_traveled
ros2 param set /patrol_node linear_speed 4.0     # takes effect immediately
ros2 service call /reset_patrol std_srvs/srv/Trigger
rqt_graph
```

## Test

```bash
colcon test --packages-select turtle_patrol && colcon test-result --verbose
```

## Exercises

1. Add a `pause` service (`std_srvs/SetBool`) that stops the turtle.
2. Spawn a second turtle with the `/spawn` service and make it follow the first.
3. Replace the proportional controller with a PID (see the next project).
