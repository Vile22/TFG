#!/usr/bin/env python3

import rospy, math
from geometry_msgs.msg import Twist, Pose2D #To publish velocities and tracking errors using the Pose2D message type
from nav_msgs.msg import Odometry
from gazebo_msgs.msg import ModelStates
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from math import sin, cos, pi

import sys, select, os
if os.name == 'nt':
  import msvcrt
else:
  import tty, termios

#Initialize variables (robot posture) and the offset of the outside point
x = 0
y = 0
yaw = 0
l = 0.1

vel_msg = Twist()
error_msg = Pose2D()
t = 0.0; t0 = 0.0; V_max = 0.3; W_max = 2.84; #Timer, initial time, maximum velocities [m/s, rad/s], respectively, for a burger type
T = 50.0; k = 0.15; #Trajectory period, controller gains kx = ky = k
ex = 0.0; ey = 0.0; V = 0.0; W = 0.0

def odomCallback(msg): #Callback function to get the robot posture
	global x; global y; global yaw
	x = msg.pose[1].position.x
	y = msg.pose[1].position.y

	#Operations to convert from quaternion to Euler angles (and vice-versa)
	quater = msg.pose[1].orientation
	quater_list = [quater.x, quater.y, quater.z, quater.w]
	(roll, pitch, yaw) = euler_from_quaternion(quater_list) #Euler angles are given in radians
	#quat = quaternion_from_euler(roll, pitch,yaw); print quat
	
def velocity_controller(): #Function to generate the desired trajectory and to compute the signals control
	global ex, ey, V, W, Xd,Yd #Indicate that some variables are global to be used in the main_function
	tray = 2

	if(tray == 2):
		#######################
		#Coordenadas lemniscata
		#######################
		a = 2; b = 1; X0 = 0; Y0 = 0; w = 2*pi/T
		#Desired position on the plane
		Xd = X0+a*sin(w*t)
		Yd = Y0+b*sin(2*w*t)
		
		#Corresponding time derivatives
		Xdp = a*w*cos(w*t)
		Ydp = 2*b*w*cos(2*w*t)

	elif(tray == 1):	
		####################
		#Coordenadas círculo
		####################
		Cx = -1.5; Cy = 0; w = 2*pi/T
		r = 1.5
		#Desired position on the plane
		Xd = Cx + r*cos(w*t)
		Yd = Cy + r*sin(w*t)

		#Corresponding time derivatives
		Xdp = -r*w*sin(w*t)
		Ydp = r*w*cos(w*t)
	
	p_x = x+l*cos(yaw); p_y = y+l*sin(yaw) #Compute the coordinates of the outside point
	ex = p_x-Xd; ey = p_y-Yd; #Compute tracking errors
	
	#Cinematic controller. Auxiliar controls, in global coordinates
	Ux = Xdp-k*ex; Uy = Ydp-k*ey
	
	#Compute the velocities according to the cinematic model for a differential type mobile robot
	V = Ux*cos(yaw)+Uy*sin(yaw)
	W = -Ux*sin(yaw)/l+Uy*cos(yaw)/l
	
	#Velocities saturation
	if (abs(V)>V_max):
		V = V_max*abs(V)/V
		print("Sat V\t")
	if (abs(W)>W_max):
		W = W_max*abs(W)/W
		print("Sat W\t")


def main_function():
	rospy.init_node('diff_robot_controller', anonymous=False) #Initialize the node
	rate = rospy.Rate(50) #Node frequency (Hz)
	counter = 0
	
	vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) #To publish in the topic
	rospy.Subscriber('/gazebo/model_states',ModelStates, odomCallback) #To subscribe to the topic

	error_pub = rospy.Publisher('/tracking_errors', Pose2D, queue_size=10)
	
	#Important: Due to a differential type mobile robot is used, the following fields are ignored
	vel_msg.linear.y = vel_msg.linear.z = vel_msg.angular.x = vel_msg.angular.y = 0
	
	error_msg.theta = 0 #Since the orientation angle is a sub-actuated state, this field is assigned equal to zero
	
	global t, t0 #t and t0 are global to be used in velocity_controller
	t0 = rospy.Time.now().to_sec()
	
	while(1):
		t = rospy.Time.now().to_sec()-t0 #Compute the controller time    
		velocity_controller() #Compute the control signals
		
		vel_msg.linear.x = V; vel_msg.angular.z = W
		vel_pub.publish(vel_msg); #Publish the control signals
	
		error_msg.x = ex; error_msg.y = ey; #Assign the tracking errors
		error_pub.publish(error_msg); #Publish the tracking errors
		
		if counter == 25:
			rospy.loginfo("t: %.2f\tex: %.3f\tey: %.3f\tV: %.3f\tW: %.2f\n", t,ex,ey,V,W) #Print in terminal some variables
			counter = 0 #Reset the counter
		else:
			counter += 1

		rate.sleep() #spinOnce() function does not exist in python
	

	#Stop the mobile robot
	vel_msg.linear.x = 0.0; vel_msg.angular.z = 0.0
	vel_pub.publish(vel_msg)
	
	print("Robot stops, but simulation keeps running\n")


if __name__ == '__main__':
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    try:
        main_function() #Execute the function
    except rospy.ROSInterruptException:
        pass