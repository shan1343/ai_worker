#!/usr/bin/env python3
#
# Copyright 2026 ROBOTIS CO., LTD.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Launch a UVC webcam such as the Logitech HD Pro Webcam C920."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context):
    camera_namespace = LaunchConfiguration('camera_namespace').perform(context)
    camera_name = LaunchConfiguration('camera_name').perform(context)
    video_device = LaunchConfiguration('video_device').perform(context)
    frame_id = LaunchConfiguration('frame_id').perform(context)
    image_width = int(LaunchConfiguration('image_width').perform(context))
    image_height = int(LaunchConfiguration('image_height').perform(context))
    pixel_format = LaunchConfiguration('pixel_format').perform(context)
    output_encoding = LaunchConfiguration('output_encoding').perform(context)

    webcam_node = Node(
        package='v4l2_camera',
        executable='v4l2_camera_node',
        namespace=camera_namespace,
        name=camera_name,
        output='screen',
        parameters=[{
            'video_device': video_device,
            'camera_frame_id': frame_id,
            'image_size': [image_width, image_height],
            'pixel_format': pixel_format,
            'output_encoding': output_encoding,
            'use_sensor_data_qos': True,
        }],
    )

    return [webcam_node]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'camera_namespace',
            default_value='webcam',
            description='Namespace for webcam image and camera_info topics.',
        ),
        DeclareLaunchArgument(
            'camera_name',
            default_value='c920',
            description='ROS node name for the webcam.',
        ),
        DeclareLaunchArgument(
            'video_device',
            default_value='/dev/video20',
            description='Linux V4L2 device path for the C920 webcam.',
        ),
        DeclareLaunchArgument(
            'frame_id',
            default_value='c920_camera_optical_frame',
            description='Frame ID stamped on published image messages.',
        ),
        DeclareLaunchArgument(
            'image_width',
            default_value='640',
            description='Requested image width in pixels.',
        ),
        DeclareLaunchArgument(
            'image_height',
            default_value='480',
            description='Requested image height in pixels.',
        ),
        DeclareLaunchArgument(
            'pixel_format',
            default_value='YUYV',
            description='Requested V4L2 pixel format. YUYV is a safe default for C920.',
        ),
        DeclareLaunchArgument(
            'output_encoding',
            default_value='rgb8',
            description='ROS image encoding published by v4l2_camera.',
        ),
        OpaqueFunction(function=launch_setup),
    ])
