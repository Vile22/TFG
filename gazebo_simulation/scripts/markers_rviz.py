#!/usr/bin/env python
"""ROS node that performs Visualization of Gas Information in RViz of ARTUR nose"""

import rospy
from geometry_msgs.msg import Point32, Point, PoseWithCovarianceStamped, Pose, Vector3, Quaternion,Twist
from visualization_msgs.msg import Marker
from std_msgs.msg import Header, ColorRGBA, String
import numpy as np
import statistics

size_anchor=0.2


class MarkerBasics(object):
	
	def __init__ (self):
		self.count=0
		
		self.marker_publisher1=rospy.Publisher('marker_p1', Marker, queue_size=5)
		self.marker_publisher2=rospy.Publisher('marker_p2', Marker, queue_size=5)
		self.marker_publisher3=rospy.Publisher('marker_p3', Marker, queue_size=5)
		self.marker_publisher4=rospy.Publisher('marker_p4', Marker, queue_size=5)

		#Publisher de las medias
		
		self.rate=rospy.Rate(1)
		
		self.p1x=0
		self.p2x=0
		self.p3x=0
		self.p4x=0
		self.p1y=0
		self.p2y=0
		self.p3y=0
		self.p4y=0
		self.p1z=0
		self.p2z=0
		self.p3z=0
		self.p4z=0
		
		
	def rviz_vis(self,*args):	
		
		lifetime_marker=8
		#Marker del punto 1
		self.markerp1=Marker()
		self.markerp1=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(self.p1x,self.p1y,self.p1z),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='robot_base_link'),
			header=Header(frame_id='robot_map'),
			color=ColorRGBA(1.0,0.0,0.0, 1))
		self.markerp1.id=self.count
		self.marker_publisher1.publish(self.markerp1)
		
		
		#Marker del punto 2
		self.markerp2=Marker()
		self.markerp2=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(self.p2x,self.p2y,self.p2z),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='robot_base_link'),
			header=Header(frame_id='robot_map'),
			color=ColorRGBA(1.0,0.0,0.0, 1))
		self.markerp2.id=self.count
		self.marker_publisher2.publish(self.markerp2)
		
		#Marker del punto 3
		self.markerp3=Marker()
		self.markerp3=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(self.p3x,self.p3y,self.p3z),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='robot_base_link'),
			header=Header(frame_id='robot_map'),
			color=ColorRGBA(1.0,0.0,0.0, 1))
		self.markerp3.id=self.count
		self.marker_publisher3.publish(self.markerp3)
				
		#Marker del punto 4
		self.markerp4=Marker()
		self.markerp4=Marker(
			type=Marker.SPHERE,
			id=0,
			lifetime=rospy.Duration(lifetime_marker),
			pose=Pose(Point(self.p4x,self.p4y,self.p4z),Quaternion(0, 0, 0, 1)),
			scale=Vector3(size_anchor,size_anchor,size_anchor),
			#header=Header(frame_id='base_link'),
			header=Header(frame_id='robot_map'),
			color=ColorRGBA(1.0,0.0,0.0, 1))
		self.markerp4.id=self.count
		self.marker_publisher4.publish(self.markerp4)
    
	def callback_p1(self,msg):	
		self.p1x=msg.position.x
		self.p1y=msg.position.y
	def callback_p2(self,msg):	
		self.p2x=msg.position.x
		self.p2y=msg.position.y
	def callback_p3(self,msg):	
		self.p3x=msg.position.x
		self.p3y=msg.position.y
	def callback_p4(self,msg):	
		self.p4x=msg.position.x
		self.p4y=msg.position.y
	
	def start(self):			
			rospy.Subscriber("/candidate_point_1",Pose,self.callback_p1)
			rospy.Subscriber("/candidate_point_2",Pose,self.callback_p2)
			rospy.Subscriber("/candidate_point_3",Pose,self.callback_p3)
			rospy.Subscriber("/candidate_point_4",Pose,self.callback_p4)
			
			rospy.Timer(rospy.Duration(2.0),self.rviz_vis)
			#self.rate.sleep()
			rospy.spin()
	
   
if __name__ == '__main__':
    rospy.init_node('marker_basic_node',anonymous=True)
    markerbasics_object=MarkerBasics()
    
    try:
		markerbasics_object.start()
		
    except rospy.ROSInterruptException:
        pass
