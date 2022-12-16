#!/usr/bin/env python3

#*********************************************************************************************************
#2022-12-15  AdMire Technologies 
#ROS2 code that subscribes to /joy topic from gamepad.
#If button[1] is pressed the number 2.0 is sent to micro-controller
#otherwise, the number 1.0 is sent to micro-controller.
#This was developped as a proof of concept porgram.  Intention is that micro-controller will activate a 
#relay that controls powerful LED on a robot.
#Communictation tested on a Teensy 4.1
#GamePad was a PlayStation 4 running standard joy_node after being paired by bluetooth. 
#ROS2 Humble running on Ubuntu 22.02
#Please do not use this code on any life critical tasks, other than that, it is free to use.
#********************************************************************************************************

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_msgs.msg import Int32
from std_msgs.msg import String
from std_msgs.msg import Header
from sensor_msgs.msg import Joy

class Ps4_control_reader(Node):
    def __init__(self):
        self.joy = Joy()
        self.joy.header = Header()
        self.joy.header.frame_id = ''
        #self.joy.axes = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        #self.joy.buttons = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        super().__init__ ("ps4_control_reader")
        self.subscriber = self.create_subscription(Joy ,"joy", self.callback_joy,1)
        self.joy=Joy()
        self.publisher = self.create_publisher(Float32, "micro_ros_arduino_subscriber", 1)
     
    def callback_joy (self, msg:Joy):
        x=int(msg.buttons[0])
        msgTeensy = Float32()
        if x==1:          
            msgTeensy.data=2.0
        else:
            msgTeensy.data=1.0   
        self.publisher.publish(msgTeensy)
        self.get_logger().info("We are sending a message to the Teensy and it is:"+str(msgTeensy)+".")

def main(args=None):
    rclpy.init(args=args)
    node=Ps4_control_reader()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()