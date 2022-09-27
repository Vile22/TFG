#!/usr/bin/env python
"""ROS node that performs Visualization of Pose in RViz of Pozyx Tag"""

import rospy
from geometry_msgs.msg import Point32, Point, Pose
from visualization_msgs.msg import Marker
global posx, posy, posz, orix, oriy, oriz, oriw, size_anchor
posx=0
posy=0
posz=0
orix=0
oriy=0
oriz=0
oriw=0
size_anchor=0.5

class MarkerBasics(object):
	global posx, posy, posz, orix, oriy, oriz, oriw
	
	def __init__ (self):
		self.marker_objectlisher=rospy.Publisher('marker_basic', Marker, queue_size=1)
		self.rate=rospy.Rate(20)
		self.init_marker(index=0,z_val=0)
	
	def init_marker(self, index=0, z_val=0):
		#Marker for tag		
		self.marker_object=Marker()
		self.marker_object.header.frame_id="/my_frame"
		self.marker_object.header.stamp=rospy.get_rostime()
		self.marker_object.ns="some_robot"
		self.marker_object.id=index
		self.marker_object.type=Marker.CUBE
		self.marker_object.action=Marker.ADD
		
		my_point=Point()
		my_point.z=z_val
		self.marker_object.pose.position=my_point
		
		self.marker_object.pose.orientation.x=0
		self.marker_object.pose.orientation.y=0
		self.marker_object.pose.orientation.z=0
		self.marker_object.pose.orientation.w=0
		self.marker_object.scale.x=0.3
		self.marker_object.scale.y=0.2
		self.marker_object.scale.z=0.1
		
		self.marker_object.color.r=0
		self.marker_object.color.g=1
		self.marker_object.color.b=0
		self.marker_object.color.a=1
		
		self.marker_object.lifetime=rospy.Duration(0)
		
		
	def start(self):
		while not rospy.is_shutdown():
			self.marker_object.pose.position.x=posx/1000
			self.marker_object.pose.position.y=posy/1000
			self.marker_object.pose.position.z=posz/1000
			self.marker_object.pose.orientation.x=orix
			self.marker_object.pose.orientation.y=oriy
			self.marker_object.pose.orientation.z=oriz
			self.marker_object.pose.orientation.w=oriw
		
			self.marker_objectlisher.publish(self.marker_object)
			listener()
			self.rate.sleep()
			
def listener():
    rospy.Subscriber("/pozyx_pose",Pose, callback)
    
def callback(data):	
	global posx, posy, posz, orix, oriy, oriz, oriw
	posx=data.position.x
	posy=data.position.y
	posz=data.position.z
	
	orix=data.orientation.x
	oriy=data.orientation.y
	oriz=data.orientation.z
	oriw=data.orientation.w

	
if __name__ == '__main__':
    global posx, posy, posz, orix, oriy, oriz, oriw
    rospy.init_node('marker_basic_node',anonymous=True)
    markerbasics_object=MarkerBasics()
    try:
		markerbasics_object.start()
		
    except rospy.ROSInterruptException:
        pass
