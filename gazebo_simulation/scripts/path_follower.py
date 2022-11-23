#!/usr/bin/env python3
"""

Probabilistic Road Map (PRM) Planner

author: Atsushi Sakai (@Atsushi_twi)

"""
import rospy
import math
import numpy as np
import cv2
from scipy.spatial import KDTree, distance
from geometry_msgs.msg import Twist, Vector3
from gazebo_msgs.msg import ModelStates
from PIL import Image



ptos = 20
rosRate = ptos/4
T= 1/rosRate
i=0

# parameters of path planning algorithm

N_SAMPLE = 200  # number of sample_points
N_KNN = 8  # number of edge from one sampled point
MAX_EDGE_LEN = 100.0  # [m] Maximum edge length

#parameters of simulation
nrobots=1

#parameters of navigation
kp_dist = 1 #1
ki_dist = 0.5
kd_dist = 1

kp_angle = 3.5 #3
ki_angle = 2 #2
kd_angle = 0.2

sat_dist=0.23
sat_angle=3

class prm_planner(object):

    def __init__(self):
        self.pub=rospy.Publisher('/cmd_vel',Twist,queue_size=5)
        self.rate=rospy.Rate(rosRate)
        self.index1 = 0
        self.xrobot=0
        self.yrobot=0
        self.ori_x_robot=0
        self.ori_y_robot=0
        self.ori_z_robot=0
        self.ori_w_robot=0

        t = np.linspace(0, T, ptos)
        self.pathx = []
        self.pathy = []        

        if(tray == '1'):
            #####################
            #Trayectoria circular
            #####################
            
            Cx = -1.5; Cy = 0; w = 2*math.pi/T
            r = 1.5
            for i in t:
                self.pathx.append(Cx + r*math.cos(w*i))
                self.pathy.append(Cy + r*math.sin(w*i))
            
        elif(tray == '2'):
            #######################
            #Trayectoria lemniscata
            #######################
            
            a = 0.50; b = 0.25; X0 = 0; Y0 = 0; w = 2*math.pi/T
            for i in t:
                self.pathx.append(X0+a*math.sin(w*i))
                self.pathy.append(Y0+b*math.sin(2*w*i))
        
        
    def callback(self,data):
        global i
        num_objects=np.size(data.name)
        for k in range(0,num_objects):
            word=data.name[k]
            if word == "jackal":
                self.index1=k
                
        self.xrobot=data.pose[self.index1].position.x
        self.yrobot=data.pose[self.index1].position.y
            
        #Orientacion con angulos de Euler
        self.ori_x_robot, self.ori_y_robot, self.ori_z_robot=euler_from_quaternion(data.pose[self.index1].orientation.x,data.pose[self.index1].orientation.y,data.pose[self.index1].orientation.z,data.pose[self.index1].orientation.w)
        
        #Para mover al robot lìder
        x_actual=self.xrobot
        y_actual=self.yrobot
        w_actual=self.ori_z_robot
        
        #Ir al primer punto y localizarse
        size2 = len(self.pathx)
        
        if (i<=(size2-1)):
            p1=[x_actual,y_actual]
            p3=[self.pathx[i],self.pathy[i]]
            distance1 = distance.euclidean(p1,p3)
        else:                                         ##################
            distance1 = distance.euclidean(p1,p3)     #ESTO NO ME CUADRA
            i = 0                                     ##################

        #Calculo del angulo para el setpoint al que se va
        dify=(self.pathy[i]-y_actual)
        difx=(self.pathx[i]-x_actual)
        m=dify/difx
        angle=math.atan(m)

        #Condicion de correcion de la tangente
        if (m>=0):
            if (difx<0):
                angle=angle-math.pi
        else:
            if(difx<0):
                angle=angle+math.pi
        
        err_dist1=distance1             ###################################
        err_dist2=distance1             #Para qué queremos esta variable???
        cumerror_dist=err_dist2*T  ###################################
        dererror_dist = err_dist2/T
        err_angle=angle-w_actual
        cumerror_angle=err_angle*T
        dererror_angle = err_angle/T
        
        pi_dist=kp_dist*err_dist2 + ki_dist*cumerror_dist + kd_dist*dererror_dist
        pi_angle=kp_angle*err_angle + ki_angle*cumerror_angle + kd_dist*dererror_angle
        
        #Valores de saturacion
        saturated_pi_dist=min(sat_dist,max(-sat_dist,pi_dist))
        saturated_pi_angle=min(sat_angle,max(-sat_angle,pi_angle))

        twist=Twist()
        #rospy.loginfo(err_dist1)
        if (i<size2):
            if(err_dist1<0.1):
                twist.linear.x = 0
                twist.angular.z = 0
                i=i+1
            else:
                twist.linear.x=saturated_pi_dist
                twist.angular.z=saturated_pi_angle
        
        self.pub.publish(twist)


    
    def start(self):
        #Establecer destino considerando la resolucion de gazebo
        rospy.Subscriber("/gazebo/model_states",ModelStates,self.callback)
        self.rate.sleep()
        rospy.spin()
            
def euler_from_quaternion(x, y, z, w):
        """
        Convert a quaternion into euler angles (roll, pitch, yaw)
        roll is rotation around x in radians (counterclockwise)
        pitch is rotation around y in radians (counterclockwise)
        yaw is rotation around z in radians (counterclockwise)
        """
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return roll_x, pitch_y, yaw_z # in radians  
            

if __name__ == '__main__':
    #starts the node
    tray = input("Circulo (1) o Lemniscata (2): ")
    rospy.init_node('prm_rtb')
    prm1=prm_planner()
    
    try:
            prm1.start()
    except rospy.ROSInterruptException:
            pass
            
    
