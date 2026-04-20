from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare  # ✅ 这里改对！
from launch.substitutions import Command
import os

def generate_launch_description():
    # 路径
    robot_desc_pkg = FindPackageShare(package="my_robot_description").find("my_robot_description")
    bringup_pkg    = FindPackageShare(package="my_robot_bringup").find("my_robot_bringup")

    urdf_file      = os.path.join(robot_desc_pkg, "urdf", "my_robot.urdf.xacro")
    rviz_file      = os.path.join(robot_desc_pkg, "rviz", "urdf_config.rviz")
    ctrl_file      = os.path.join(bringup_pkg, "config", "my_robot_controllers.yaml")

    robot_desc = {"robot_description": Command(["xacro ", urdf_file])}

    # 启动所有节点
    return LaunchDescription([
        # # 关节滑块
        # Node(
        #     package="joint_state_publisher_gui",
        #     executable="joint_state_publisher_gui",
        #     output="screen"
        # ),

        # 机器人状态发布
        Node(
            package="robot_state_publisher",
            executable="robot_state_publisher",
            parameters=[robot_desc],
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