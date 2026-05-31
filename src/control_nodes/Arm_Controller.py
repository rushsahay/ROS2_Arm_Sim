#!/usr/bin/env python3
import rclpy
from std_msgs.msg import Float64MultiArray
from rclpy.node import Node
import time
import numpy as np

# base_joint_position = 0 #Capped between -3.14 and 3.14 radians
# first_joint_position = 0.7 #Capped between -0.7 and 0.7 radians
# second_joint_position = 0.7 #Capped between -0.7 and 0.7 radians

#Absolute coordinates in fixed frame
x = -0.5
y = -0.5
z = 1.4

L1 = 0.6
L2 = 0.6
rot = 0.45

class Controller_Node(Node):
    def __init__(self, x,y,z):
        super().__init__("Position_Node")
        self.publisher_ = self.create_publisher(Float64MultiArray,"/arm_position_controller/commands",10)

        self.x = x
        self.y = y
        self.z = z
        # self.base_position = base_joint_position
        # self.first_position = first_joint_position
        # self.second_position = second_joint_position

        self.period = 0.05

        self.timer = self.create_timer(self.period,self.send_sequence)
        self.get_logger().info("Logger Starting")

    def send_sequence(self):
        x = self.x
        y= self.y
        z = self.z

        base_position = np.arctan2(y,x)

        r = np.sqrt(x**2+y**2)
        dz = z - rot

        D = (r**2 + dz**2 - L1**2 - L2**2) / (2 * L1 * L2)
        D = np.clip(D, -1.0, 1.0)  # numerical safety
        second_position = np.arccos(D)



        if not(-0.7<second_position<0.7):
            self.get_logger().warning("Target is unreachable with current constraints")
            second_position = np.clip(second_position[0],-0.7,0.7)

        first_position = np.arctan2(r, dz) - np.arctan2(
        L2 * np.sin(second_position),
        L1 + L2 * np.cos(second_position)
    )

        msg = Float64MultiArray()
        msg.data = [base_position,first_position,second_position]

        self.get_logger().info(f"Published target: {msg.data}")
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = Controller_Node(x,y,z)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
