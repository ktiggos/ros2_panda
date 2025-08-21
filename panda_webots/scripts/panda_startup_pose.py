#!/usr/bin/env python3
import rclpy
from rclpy.action import ActionClient
from rclpy.duration import Duration
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectoryPoint

JOINTS = [
    'panda_joint1','panda_joint2','panda_joint3',
    'panda_joint4','panda_joint5','panda_joint6','panda_joint7'
]

READY = [0.0, -0.7853981633974483, 0.0, -2.356194490192345, 0.0, 1.5707963267948966, 0.7853981633974483]

def main():
    rclpy.init()
    node = rclpy.create_node('panda_startup_pose')

    client = ActionClient(node, FollowJointTrajectory,
                          '/panda_arm_controller/follow_joint_trajectory')

    node.get_logger().info('Waiting for /panda_arm_controller/follow_joint_trajectory...')
    while not client.wait_for_server(timeout_sec=0.5):
        rclpy.spin_once(node, timeout_sec=0.1)
        node.get_logger().info('  still waiting...')

    goal = FollowJointTrajectory.Goal()
    goal.trajectory.joint_names = JOINTS

    pt = JointTrajectoryPoint()
    pt.positions = READY
    pt.time_from_start = Duration(seconds=2.0).to_msg()
    goal.trajectory.points = [pt]

    node.get_logger().info('Sending startup pose...')
    send_future = client.send_goal_async(goal)
    rclpy.spin_until_future_complete(node, send_future)
    goal_handle = send_future.result()

    if not goal_handle or not goal_handle.accepted:
        node.get_logger().error('Goal was rejected by the controller.')
        node.destroy_node()
        rclpy.shutdown()
        return

    node.get_logger().info('Goal accepted. Waiting for result...')
    result_future = goal_handle.get_result_async()
    rclpy.spin_until_future_complete(node, result_future)
    result = result_future.result()
    if result is not None:
        node.get_logger().info(f'Finished with error_code={result.result.error_code}, '
                               f'message="{getattr(result.result, "error_string", "")}"')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
