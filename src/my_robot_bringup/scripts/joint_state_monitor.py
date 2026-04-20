#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState

class JointStateMonitor(Node):
    def __init__(self):
        super().__init__('joint_state_monitor')
        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        self.get_logger().info('关节状态监控节点已启动，监听 /joint_states 话题')

    def joint_state_callback(self, msg):
        self.get_logger().info('接收到关节状态:')
        for i, name in enumerate(msg.name):
            position_deg = msg.position[i] * 180.0 / 3.14159  # 转换为度
            self.get_logger().info('.2f'
                                 '.2f')

def main(args=None):
    rclpy.init(args=args)
    node = JointStateMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()