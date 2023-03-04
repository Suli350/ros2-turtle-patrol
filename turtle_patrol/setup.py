import os
from glob import glob

from setuptools import find_packages, setup

package_name = 'turtle_patrol'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*')),
        (os.path.join('share', package_name, 'config'), glob('config/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Sulaiman',
    maintainer_email='suliman31991@gmail.com',
    description='Waypoint patrol for turtlesim: topics, services, parameters and launch files.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'patrol_node = turtle_patrol.patrol_node:main',
            'odometer_node = turtle_patrol.odometer_node:main',
        ],
    },
)
