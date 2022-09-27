#!/usr/bin/env python3
"""ROS node that performs Visualization of Pose in RViz of Pozyx Tag"""

import rospy
from geometry_msgs.msg import Point32, Point, Pose
from visualization_msgs.msg import Marker
global posx, posy, posz, orix, oriy, oriz, oriw
posx=0
posy=0
posz=0
orix=0
oriy=0
oriz=0
oriw=0
size_anchor=0.1
scale_tagx=0.075
scale_tagy=0.07
scale_tagz=0.02

#anchor coordinates
anchor1_x=rospy.get_param("/anchor1_x")
anchor1_y=rospy.get_param("/anchor1_y")
anchor1_z=rospy.get_param("/anchor1_z")

anchor2_x=rospy.get_param("/anchor2_x")
anchor2_y=rospy.get_param("/anchor2_y")
anchor2_z=rospy.get_param("/anchor2_z")

anchor3_x=rospy.get_param("/anchor3_x")
anchor3_y=rospy.get_param("/anchor3_y")
anchor3_z=rospy.get_param("/anchor3_z")

anchor4_x=rospy.get_param("/anchor4_x")
anchor4_y=rospy.get_param("/anchor4_y")
anchor4_z=rospy.get_param("/anchor4_z")

class MarkerBasics(object):
	global posx, posy, posz, orix, oriy, oriz, oriw
	
	def __init__ (self):
		self.marker_objectlisher=rospy.Publisher('marker_basic', Marker, queue_size=1)
		self.marker_objectlisher_a1=rospy.Publisher('marker_basic1', Marker, queue_size=1)
		self.marker_objectlisher_a2=rospy.Publisher('marker_basic2', Marker, queue_size=1)
		self.marker_objectlisher_a3=rospy.Publisher('marker_basic3', Marker, queue_size=1)
		self.marker_objectlisher_a4=rospy.Publisher('marker_basic4', Marker, queue_size=1)
		self.rate=rospy.Rate(20)
		self.init_marker(index=0,z_val=0)
	
	def init_marker(self, index=0, z_val=0):
		#Marker for tag		
		self.marker_object=Marker()
		self.marker_object.header.frame_id="my_frame"
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
		self.marker_object.pose.orientation.w=1
		self.marker_object.scale.x=scale_tagx
		self.marker_object.scale.y=scale_tagy
		self.marker_object.scale.z=scale_tagz
		
		self.marker_object.color.r=0
		self.marker_object.color.g=1
		self.marker_object.color.b=0
		self.marker_object.color.a=1
		
		self.marker_object.lifetime=rospy.Duration(0)
		
		#Marker for anchor 1	
		self.marker_object_a1=Marker()
		self.marker_object_a1.header.frame_id="my_frame"
		self.marker_object_a1.header.stamp=rospy.get_rostime()
		self.marker_object_a1.ns="some_robot"
		self.marker_object_a1.id=index
		self.marker_object_a1.type=Marker.SPHERE
		self.marker_object_a1.action=Marker.ADD
		
		my_point_a1=Point()
		my_point_a1.z=z_val
		self.marker_object_a1.pose.position=my_point
		self.marker_object_a1.pose.orientation.x=0
		self.marker_object_a1.pose.orientation.y=0
		self.marker_object_a1.pose.orientation.z=0		
		self.marker_object_a1.pose.orientation.w=1
		
		self.marker_object_a1.scale.x=size_anchor
		self.marker_object_a1.scale.y=size_anchor
		self.marker_object_a1.scale.z=size_anchor
		
		self.marker_object_a1.color.r=1
		self.marker_object_a1.color.g=0
		self.marker_object_a1.color.b=0
		self.marker_object_a1.color.a=1
		
		#Marker for anchor 2	
		self.marker_object_a2=Marker()
		self.marker_object_a2.header.frame_id="my_frame"
		self.marker_object_a2.header.stamp=rospy.get_rostime()
		self.marker_object_a2.ns="some_robot"
		self.marker_object_a2.id=index
		self.marker_object_a2.type=Marker.SPHERE
		self.marker_object_a2.action=Marker.ADD
		
		my_point_a2=Point()
		my_point_a2.z=z_val
		self.marker_object_a2.pose.position=my_point

		self.marker_object_a2.pose.orientation.x=0
		self.marker_object_a2.pose.orientation.y=0
		self.marker_object_a2.pose.orientation.z=0		
		self.marker_object_a2.pose.orientation.w=1

		self.marker_object_a2.scale.x=size_anchor
		self.marker_object_a2.scale.y=size_anchor
		self.marker_object_a2.scale.z=size_anchor
		
		self.marker_object_a2.color.r=1
		self.marker_object_a2.color.g=0
		self.marker_object_a2.color.b=0
		self.marker_object_a2.color.a=1
		
		#Marker for anchor 3	
		self.marker_object_a3=Marker()
		self.marker_object_a3.header.frame_id="my_frame"
		self.marker_object_a3.header.stamp=rospy.get_rostime()
		self.marker_object_a3.ns="some_robot"
		self.marker_object_a3.id=index
		self.marker_object_a3.type=Marker.SPHERE
		self.marker_object_a3.action=Marker.ADD
		
		my_point_a3=Point()
		my_point_a3.z=z_val
		self.marker_object_a3.pose.position=my_point
		
		self.marker_object_a3.pose.orientation.x=0
		self.marker_object_a3.pose.orientation.y=0
		self.marker_object_a3.pose.orientation.z=0		
		self.marker_object_a3.pose.orientation.w=1
		
		self.marker_object_a3.scale.x=size_anchor
		self.marker_object_a3.scale.y=size_anchor
		self.marker_object_a3.scale.z=size_anchor
		
		self.marker_object_a3.color.r=1
		self.marker_object_a3.color.g=0
		self.marker_object_a3.color.b=0
		self.marker_object_a3.color.a=1
		
		#Marker for anchor 4	
		self.marker_object_a4=Marker()
		self.marker_object_a4.header.frame_id="my_frame"
		self.marker_object_a4.header.stamp=rospy.get_rostime()
		self.marker_object_a4.ns="some_robot"
		self.marker_object_a4.id=index
		self.marker_object_a4.type=Marker.SPHERE
		self.marker_object_a4.action=Marker.ADD
		
		my_point_a4=Point()
		my_point_a4.z=z_val
		self.marker_object_a4.pose.position=my_point

		self.marker_object_a4.pose.orientation.x=0
		self.marker_object_a4.pose.orientation.y=0
		self.marker_object_a4.pose.orientation.z=0		
		self.marker_object_a4.pose.orientation.w=1
		
		self.marker_object_a4.scale.x=size_anchor
		self.marker_object_a4.scale.y=size_anchor
		self.marker_object_a4.scale.z=size_anchor
		
		self.marker_object_a4.color.r=1
		self.marker_object_a4.color.g=0
		self.marker_object_a4.color.b=0
		self.marker_object_a4.color.a=1
		
		self.marker_object_a4.lifetime=rospy.Duration(0)
		
		
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
			
			self.marker_object_a1.pose.position.x=anchor1_x/1000
			self.marker_object_a1.pose.position.y=anchor1_y/1000
			self.marker_object_a1.pose.position.z=anchor1_z/1000
		
			self.marker_objectlisher_a1.publish(self.marker_object_a1)
			
			
			self.marker_object_a2.pose.position.x=anchor2_x/1000
			self.marker_object_a2.pose.position.y=anchor2_y/1000
			self.marker_object_a2.pose.position.z=anchor2_z/1000
			
			self.marker_objectlisher_a2.publish(self.marker_object_a2)
			
			self.marker_object_a3.pose.position.x=anchor3_x/1000
			self.marker_object_a3.pose.position.y=anchor3_y/1000
			self.marker_object_a3.pose.position.z=anchor3_z/1000
			
			self.marker_objectlisher_a3.publish(self.marker_object_a3)
			
			self.marker_object_a4.pose.position.x=anchor4_x/1000
			self.marker_object_a4.pose.position.y=anchor4_y/1000
			self.marker_object_a4.pose.position.z=anchor4_z/1000
			
			self.marker_objectlisher_a4.publish(self.marker_object_a4)
			
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
	posx, posy, posz, orix, oriy, oriz, oriw
	rospy.init_node('marker_basic_node',anonymous=True)
	markerbasics_object=MarkerBasics()
	try:
		markerbasics_object.start()
		
	except rospy.ROSInterruptException:
		pass
