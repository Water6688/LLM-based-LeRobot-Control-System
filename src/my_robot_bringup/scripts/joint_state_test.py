#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import time

class JointStateTest(Node):
    def __init__(self):
        super().__init__('joint_state_test')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        self.publisher = self.create_publisher(JointState, '/joint_states', 10)
        self.timer = self.create_timer(1.0, self.publish_test_state)
        self.get_logger().info('关节状态测试节点已启动')

    def joint_state_callback(self, msg):
        self.get_logger().info(f'接收到关节状态: {len(msg.name)} 个关节')
        for i, name in enumerate(msg.name):
            position_deg = msg.position[i] * 180.0 / 3.14159
            self.get_logger().info('.2f')

    def publish_test_state(self):
        # 发布测试关节状态
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6']
        msg.position = [0.1, 0.2, -0.1, 0.0, 0.0, 0.0]  # 测试角度
        msg.velocity = [0.0] * 6
        msg.effort = [0.0] * 6

        self.publisher.publish(msg)
        self.get_logger().info('发布测试关节状态')

def main(args=None):
    rclpy.init(args=args)
    node = JointStateTest()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()