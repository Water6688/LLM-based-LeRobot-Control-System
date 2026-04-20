from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, PathJoinSubstitution
import os

def generate_launch_description():
    # 路径
    robot_desc_pkg = FindPackageShare(package="my_robot_description")
    bringup_pkg = FindPackageShare(package="my_robot_bringup")

    urdf_file = PathJoinSubstitution([robot_desc_pkg, "urdf", "my_robot.urdf.xacro"])
    rviz_file = PathJoinSubstitution([robot_desc_pkg, "rviz", "urdf_config.rviz"])
    ctrl_file = PathJoinSubstitution([bringup_pkg, "config", "my_robot_controllers.yaml"])
    world_file = PathJoinSubstitution([bringup_pkg, "worlds", "empty.world"])

    robot_desc = {"robot_description": Command(["xacro ", urdf_file])}

    # 启动所有节点
    return LaunchDescription([
        # 机器人状态发布
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[robot_desc],
            output="screen"
        ),

        # Gazebo
        ExecuteProcess(
            cmd=["gazebo", "--verbose", "-s", "libgazebo_ros_init.so", "-s", "libgazebo_ros_factory.so", world_file],
            output="screen"
        ),

        # 加载机器人到Gazebo
        Node(
            package="gazebo_ros",
            executable="spawn_entity.py",
            arguments=["-topic", "robot_description", "-entity", "my_robot"],
            output="screen"
        ),

        # ros2_control 核心
        Node(
            package="controller_manager",
            executable="ros2_control_node",
            parameters=[robot_desc, ctrl_file],
            output="screen"
        ),

        # 控制器
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["joint_state_broadcaster"],
            output="screen"
        ),
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["arm_controller"],
            output="screen"
        ),
        Node(
            package="controller_manager",
            executable="spawner",
            arguments=["gripper_controller"],
            output="screen"
        ),

        # RVIZ
        Node(
            package="rviz2",
            executable="rviz2",
            arguments=["-d", rviz_file],
            output="screen"
        ),
    ])