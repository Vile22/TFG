#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Point32, Point, Pose
import numpy as np
from math import sin, cos, pi, sqrt
from visualization_msgs.msg import Marker, MarkerArray
global posx, posy, posz, orix, oriy, oriz, oriw, size_anchor
posx=0
posy=0
posz=0
orix=0
oriy=0
oriz=0
oriw=0
X = []
Y = []
i = 0
T = 50

class MarkerBasics(object):
    global posx, posy, posz, orix, oriy, oriz, oriw
	
    def __init__ (self):
        global posx, posy
        #self.marker_objectlisher=rospy.Publisher('/visualization_marker', Marker, queue_size=1)
        self.marker_arraylisher=rospy.Publisher('/visualization_marker_array', MarkerArray, queue_size=10)
        ptos = 40
        self.rate=rospy.Rate(ptos+1)
        
        t = np.linspace(0, T, ptos)
        tray = 2

        if(tray == 1):
            #####################
            #Trayectoria circular
            #####################
            
            Cx = -1.5; Cy = 0; w = 2*pi/T
            r = 1.5
            for i in t:
                X.append(Cx + r*cos(w*i))
                Y.append(Cy + r*sin(w*i))
            
        elif(tray == 2):
            #######################
            #Trayectoria lemniscata
            #######################
            
            a = 2; b = 1; X0 = 0; Y0 = 0; w = 2*pi/T
            for i in t:
                X.append(X0+a*sin(w*i))
                Y.append(Y0+b*sin(2*w*i))
        

        self.init_marker(index=0,z_val=0)
	
    def init_marker(self, index=0, z_val=0):
        #Marker for tag	
        self.marker_array = MarkerArray()	
        self.marker_object = Marker()
        self.marker_object.header.frame_id = 'odom'
        self.marker_object.header.stamp = rospy.get_rostime()
        self.marker_object.ns = "map"
        self.marker_object.id = index
        self.marker_object.type = Marker.SPHERE
        self.marker_object.action = Marker.ADD

        my_point=Point()
        my_point.z=z_val
        self.marker_object.pose.position=my_point

        self.marker_object.pose.orientation.x=0
        self.marker_object.pose.orientation.y=0
        self.marker_object.pose.orientation.z=0
        self.marker_object.pose.orientation.w=0
        self.marker_object.scale.x=0.15
        self.marker_object.scale.y=0.15
        self.marker_object.scale.z=0.15

        self.marker_object.color.r=0
        self.marker_object.color.g=1
        self.marker_object.color.b=0
        self.marker_object.color.a=1

        self.marker_object.lifetime=rospy.Duration(0)
		
		
    def start(self):
        global i
        while not rospy.is_shutdown():
            self.marker_object.id = i
            self.marker_object.pose.position.x=posx
            self.marker_object.pose.position.y=posy
            self.marker_object.pose.position.z=posz
            self.marker_object.pose.orientation.x=orix
            self.marker_object.pose.orientation.y=oriy
            self.marker_object.pose.orientation.z=oriz
            self.marker_object.pose.orientation.w=oriw
            if(i < len(X)):
                self.marker_array.markers.append(self.marker_object)
                rospy.loginfo(self.marker_array.markers[i].id)
                #self.marker_objectlisher.publish(self.marker_object)
                self.marker_arraylisher.publish(self.marker_array)
                rospy.sleep(0.5)
                #self.rate.sleep()
            actualiza_coord()



def actualiza_coord():
    global posx, posy, i, id
    if(i < len(X)):
        posx = X[i]
        posy = Y[i]
        i += 1
        
'''
def listener():
    rospy.Subscriber("/pozyx_pose",Pose, callback)
'''
'''
def callback(data):	
	global posx, posy, posz, orix, oriy, oriz, oriw
	posx=data.position.x
	posy=data.position.y
	posz=data.position.z
	
	orix=data.orientation.x
	oriy=data.orientation.y
	oriz=data.orientation.z
	oriw=data.orientation.w
'''
	
if __name__ == '__main__':
    rospy.init_node('marker_basic_node',anonymous=True)
    markerbasics_object=MarkerBasics()
    try:
        markerbasics_object.start()
		
    except rospy.ROSInterruptException:
        pass






'''
import rospy
from math import sin, cos, pi
import numpy as np
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point

X = []
Y = []
posx = 0
posy = 0
class MarkerBasics(object):
    global posx, posy

    def __init__(self):
        global posx, posy
        self.marker_pub = rospy.Publisher('marker_basic', Marker, queue_size = 1)
        self.rate = rospy.Rate(20)

        ptos = 10
        t = np.linspace(0, 2*pi, ptos)

        #####################
        #Trayectoria circular
        #####################

        Cx = -1.5; Cy = 0
        r = 1.5
        for i in t:
            X.append(Cx + r*cos(i))
            Y.append(Cy + r*sin(i))

        posx = X[0]
        posy = Y[0]
        self.init_marker(index=0, z_val=0)

    def init_marker(self, index=0, z_val=0):
        self.m = Marker()
        self.m.header.frame_id = "/my_frame"
        self.m.header.stamp = rospy.get_rostime()
        self.m.ns = "some_robot"
        self.m.id = index
        self.m.type = Marker.SPHERE
        self.m.action = Marker.ADD

        my_point = Point()
        my_point.z = z_val
        self.m.pose.position = my_point

        self.m.pose.orientation.x = 0
        self.m.pose.orientation.y = 0
        self.m.pose.orientation.z = 0
        self.m.pose.orientation.w = 0

        # Introducimos medidas del marcador
        self.m.scale.x = 1
        self.m.scale.y = 1
        self.m.scale.z = 1
        # Escogemos el color
        self.m.color.r = 0
        self.m.color.g = 1
        self.m.color.b = 0
        self.m.color.a = 1

        self.m.lifetime = rospy.Duration(10)
        

    def start(self):
        while not rospy.is_shutdown():
            # Asignamos coordenadas al marcador
            self.m.pose.position.x = 1000
            self.m.pose.position.y = 1000
            self.m.pose.position.z = 0
            self.m.pose.orientation.x = 0
            self.m.pose.orientation.y = 0
            self.m.pose.orientation.z = 0
            self.m.pose.orientation.w = 0

            #actualiza_coord()

            self.marker_pub.publish()
            self.rate.sleep()

def actualiza_coord():
    global posx, posy
    i = 1
    if(i < len(X)):
        posx = X[i]
        posy = Y[i]
        i = i+1

if __name__ == '__main__':
    rospy.init_node('marker_basic_node', anonymous = True)
    Circulo = MarkerBasics()
    try:        
        Circulo.start()
    except rospy.ROSInterruptException:
        pass
'''