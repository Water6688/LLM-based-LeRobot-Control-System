#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time

class AngleTestNode(Node):
    def __init__(self):
        super().__init__('angle_test_node')
        self.arm_publisher = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )
        self.get_logger().info('角度同步测试节点已启动')

        # 测试序列：0度 -> 30度 -> -30度 -> 0度
        self.test_sequence = [
            [0.0, 0.0, 0.0, 0.0, 0.0],  # 所有关节0度（对应舵机2048）
            [0.5236, 0.0, 0.0, 0.0, 0.0],  # joint1 30度
            [-0.5236, 0.0, 0.0, 0.0, 0.0], # joint1 -30度
            [0.0, 0.0, 0.0, 0.0, 0.0],   # 回到0度
        ]
        self.current_test = 0
        self.timer = self.create_timer(3.0, self.send_test_command)

    def send_test_command(self):
        if self.current_test >= len(self.test_sequence):
            self.get_logger().info('角度同步测试完成')
            return

        trajectory = JointTrajectory()
        trajectory.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5']

        point = JointTrajectoryPoint()
        point.positions = self.test_sequence[self.current_test]
        point.time_from_start = Duration(sec=2, nanosec=0)

        trajectory.points.append(point)

        self.arm_publisher.publish(trajectory)
        self.get_logger().info(f'发送测试命令 {self.current_test + 1}: 关节角度 = {self.test_sequence[self.current_test]}')

        self.current_test += 1

def main(args=None):
    rclpy.init(args=args)
    node = AngleTestNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()