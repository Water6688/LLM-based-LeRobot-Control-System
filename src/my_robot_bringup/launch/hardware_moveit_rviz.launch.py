from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from moveit_configs_utils import MoveItConfigsBuilder
import os


def generate_launch_description():
    usb_port_arg = DeclareLaunchArgument(
        "usb_port",
        default_value="/dev/ttyUSB0",
        description="Serial device for STS3215 controller",
    )

    robot_desc_pkg = FindPackageShare(package="my_robot_description").find("my_robot_description")
    moveit_pkg = FindPackageShare(package="my_robot_moveit_config").find("my_robot_moveit_config")
    bringup_pkg = FindPackageShare(package="my_robot_bringup").find("my_robot_bringup")
    urdf_file = os.path.join(robot_desc_pkg, "urdf", "my_robot.urdf.xacro")
    rviz_file = os.path.join(moveit_pkg, "config", "moveit.rviz")
    ctrl_file = os.path.join(bringup_pkg, "config", "my_robot_controllers.yaml")

    robot_description = {
        "robot_description": Command(
            [
                "xacro ",
                urdf_file,
                " use_simulation_ros2_control:=false",
                " use_hardware_ros2_control:=true",
                " read_only:=false",
                " usb_port:=",
                LaunchConfiguration("usb_port"),
            ]
        )
    }

    moveit_config = MoveItConfigsBuilder("my_robot", package_name="my_robot_moveit_config").to_moveit_configs()

    return LaunchDescription(
        [
            usb_port_arg,
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                parameters=[robot_description],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="ros2_control_node",
                parameters=[robot_description, ctrl_file],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["joint_state_broadcaster"],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["arm_controller"],
                output="screen",
            ),
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=["gripper_controller"],
                output="screen",
            ),
            Node(
                package="moveit_ros_move_group",
                executable="move_group",
                output="screen",
                parameters=[robot_description, moveit_config.to_dict()],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                arguments=["-d", rviz_file],
                parameters=[
                    robot_description,
                    moveit_config.robot_description_semantic,
                    moveit_config.robot_description_kinematics,
                    moveit_config.joint_limits,
                    moveit_config.planning_pipelines,
                ],
                output="screen",
            ),
        ]
    )