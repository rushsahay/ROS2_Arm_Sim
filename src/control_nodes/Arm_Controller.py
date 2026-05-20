#!/usr/bin/env python3
import rclpy
from std_msgs.msg import Float64MultiArray
from rclpy.node import Node
import time

base_joint_position = 1.57 #Capped between -3.14 and 3.14 radians
first_joint_position = 0.7 #Capped between -0.7 and 0.7 radians
second_joint_position = -0.7 #Capped between -0.7 and 0.7 radians

class Controller_Node(Node):
    def __init__(self, base_joint_position,first_joint_position,second_joint_position):
        super().__init__("Position_Node")
        self.publisher_ = self.create_publisher(Float64MultiArray,"/arm_position_controller/commands",10)
        self.base_position = base_joint_position
        self.first_position = first_joint_position
        self.second_position = second_joint_position

        self.period = 0.05

        self.timer = self.create_timer(self.period,self.send_sequence)
        self.get_logger().info("Logger Starting")

    def send_sequence(self):
        # setpoints = [
        #     [1.57,0.3,-0.4],
        #     [0.0,0.0,0.0],
        #     [-1.57,-0.3,0.2],
        #     [0.0,0.5,0.5]]

        # for target in setpoints:
        #     msg = Float64MultiArray()
        #     msg.data = target

        #     self.get_logger().info(f"Publishing target: {target}")
        #     self.publisher_.publish(msg) 

        #     time.sleep(4)
        base_position = self.base_position
        first_position = self.first_position
        second_position = self.second_position
        msg = Float64MultiArray()
        msg.data = [base_position,first_position,second_position]

        self.get_logger().info(f"Published target: {msg.data}")
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Controller_Node(base_joint_position,first_joint_position,second_joint_position)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
