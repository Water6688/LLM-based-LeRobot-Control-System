#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller_test')
        self.arm_publisher = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )
        self.gripper_publisher = self.create_publisher(
            JointTrajectory,
            '/gripper_controller/joint_trajectory',
            10
        )
        self.timer = self.create_timer(5.0, self.send_trajectory)

    def send_trajectory(self):
        # 创建关节轨迹消息
        trajectory = JointTrajectory()
        trajectory.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5']

        # 创建轨迹点
        point = JointTrajectoryPoint()
        point.positions = [0.5, 0.3, -0.2, 0.1, 0.0]  # 目标位置
        point.time_from_start = Duration(sec=2, nanosec=0)

        trajectory.points.append(point)

        self.arm_publisher.publish(trajectory)
        self.get_logger().info('发送机械臂轨迹命令')

        # 夹爪控制
        gripper_trajectory = JointTrajectory()
        gripper_trajectory.joint_names = ['joint6']

        gripper_point = JointTrajectoryPoint()
        gripper_point.positions = [0.5]  # 张开夹爪
        gripper_point.time_from_start = Duration(sec=1, nanosec=0)

        gripper_trajectory.points.append(gripper_point)

        self.gripper_publisher.publish(gripper_trajectory)
        self.get_logger().info('发送夹爪轨迹命令')

def main(args=None):
    rclpy.init(args=args)
    node = ArmController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()