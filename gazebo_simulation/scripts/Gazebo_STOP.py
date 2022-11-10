#!/usr/bin/env python3
from logging import shutdown
import rospy
from geometry_msgs.msg import Twist, Vector3, Pose2D
from gazebo_msgs.msg import ModelStates
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Joy
from turtlesim.msg import Pose
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from math import sin, cos, pi, sqrt
import numpy as np
import matplotlib.pyplot as plt


ptos = 200
rosRate = 1/(2*pi/ptos)
delta_t = 1/rosRate
X = []
Y = []
Xsr = []
Ysr = []
Xd = []
Yd = []
index = 0
fig, ax = plt.subplots()
V_max = 0.22; W_max = 2
yaw = 0
l = 0.1
x = 0
y = 0
V = 0
W = 0
t0 = 0
t1 = 0

class teleop_walle(object):

    def __init__ (self):
        self.vel_pub = rospy.Publisher('/cmd_vel', Twist,queue_size=10)
        self.error_pub = rospy.Publisher('/tracking_errors', Pose2D, queue_size=10)
        self.rate=rospy.Rate(rosRate)
        self.linear_speed=0
        self.angular_speed=0
        self.deadman_walle=0
		#Ajuste de programa main
        self.vel_msg = Twist()
        self.error_msg = Pose2D()
        self.vel_msg.linear.y = self.vel_msg.linear.z = self.vel_msg.angular.x = self.vel_msg.angular.y = 0
        

    def odom_callback(self,data):
        global t0,x,y,delta_t, yaw, ex, ey, V, W, Xd,Yd, t, t_ant, t0 #t and t0 are global to be used in velocity_controller
        
        self.deadman_walle=1
        self.error_msg.theta = 0 #Since the orientation angle is a sub-actuated state, this field is assigned equal to zero
        t0 = rospy.Time.now().to_sec()

        self.vel_msg.linear.x = V
        self.vel_msg.angular.z = W
        
        if (self.deadman_walle==1):
            twist = Twist()
			#Para mandar a publicar velocidades del summit
            twist.linear.x = self.vel_msg.linear.x
            twist.angular.z = self.vel_msg.angular.z
			
            self.vel_pub.publish(twist)
        else:
            twist = Twist()
            self.vel_pub.publish(twist)
    
            

    def start(self):
        global V,W,X,Y,delta_t,Xd,Yd,t
        V = 0
        W = 0
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.odom_callback)
        self.rate.sleep()
        rospy.spin()



if __name__ == '__main__':
    rospy.init_node('joy_walle')
    teleop1=teleop_walle()

    try:
        rospy.Timer(rospy.Duration(delta_t), teleop1.start())
    except rospy.ROSInterruptException:
        pass
