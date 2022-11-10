#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import Joy
# Author: Andrew Dai
# This ROS Node converts Joystick inputs from the joy node
# into commands for turtlesim

# Receives joystick messages (subscribed to Joy topic)
# then converts the joysick inputs into Twist commands
# axis 1 aka left stick vertical controls linear speed
# axis 0 aka left stick horizonal controls angular speed

rosRate=50


class teleop_walle(object):
	def __init__ (self):
		self.pub = rospy.Publisher('/cmd_vel', Twist,queue_size=1)
		self.rate=rospy.Rate(rosRate)
		self.linear_speed=0
		self.angular_speed=0
		self.deadman_walle=0

	def callback(self,data):
		
		self.linear_speed=scale_linear*data.axes[1]
		self.linear_speed=scale_linear*data.axes[0]
		self.deadman_walle=data.buttons[5]

		if (self.deadman_walle==1):
			twist = Twist()
			#Para mandar a publicar velocidades del summit
			twist.linear.x = self.linear_speed
			twist.angular.z = self.angular_speed
			
			self.pub.publish(twist)
		else:
			twist = Twist()
			self.pub.publish(twist)
			
		
    # Intializes everything
	def start(self):
		# subscribed to joystick inputs on topic "joy"
		rospy.Subscriber("joy", Joy, self.callback)
		#while not rospy.is_shutdown():
		self.rate.sleep()
		rospy.spin()
	
if __name__ == '__main__':
	# starts the node
	rospy.init_node('joy_walle')
	teleop1=teleop_walle()
	try:
			teleop1.start()
	except rospy.ROSInterruptException:
			pass
