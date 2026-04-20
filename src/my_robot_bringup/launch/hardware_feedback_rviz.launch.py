from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, LaunchConfiguration
import os


def generate_launch_description():
    usb_port_arg = DeclareLaunchArgument(
        "usb_port",
        default_value="/dev/ttyUSB0",
        description="Serial device for STS3215 controller",
    )

    robot_desc_pkg = FindPackageShare(package="my_robot_description").find("my_robot_description")
    bringup_pkg = FindPackageShare(package="my_robot_bringup").find("my_robot_bringup")

    urdf_file = os.path.join(robot_desc_pkg, "urdf", "my_robot.urdf.xacro")
    rviz_file = os.path.join(robot_desc_pkg, "rviz", "urdf_config.rviz")
    ctrl_file = os.path.join(bringup_pkg, "config", "my_robot_feedback_only.yaml")

    robot_desc = {
        "robot_description": Command(
            [
                "xacro ",
                urdf_file,
                " use_simulation_ros2_control:=false",
                " use_hardware_ros2_control:=true",
                " read_only:=true",
                " usb_port:=",
                LaunchConfiguration("usb_port"),
            ]
        )
    }

    return LaunchDescription(
        [
            usb_port_arg,
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[robot_desc],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="ros2_control_node",
                parameters=[robot_desc, ctrl_file],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["joint_state_broadcaster"],
                output="screen",
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=["-d", rviz_file],
                output="screen",
            ),
        ]
    )
