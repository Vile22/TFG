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


ptos = 10
rosRate = 1/(2*pi/(ptos-1))
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
        
        self.pose_jack=data
        x=self.pose_jack.pose[1].position.x
        y=self.pose_jack.pose[1].position.y
        yaw=self.pose_jack.pose[1].orientation.w
        self.deadman_walle=1
		
        
		
        self.error_msg.theta = 0 #Since the orientation angle is a sub-actuated state, this field is assigned equal to zero
        t0 = rospy.Time.now().to_sec()
        self.velocity_controller() #Compute the control signals

        self.vel_msg.linear.x = V
        self.vel_msg.angular.z = W
        
        if (self.deadman_walle==1):
            twist = Twist()
			#Para mandar a publicar velocidades del summit
            twist.linear.x = self.vel_msg.linear.x
            twist.angular.z = self.vel_msg.angular.z
			
            self.vel_pub.publish(twist)
        else:
            if(error<=1):
                twist = Twist()
                self.vel_pub.publish(twist)



    def velocity_controller(self):
        global index,V,W,t,t1,error

        if(index != len(Xd)-1):
            error = sqrt((X[index]-x)**2+(Y[index]-y)**2)
            '''
            rospy.loginfo("------------------------------")
            rospy.loginfo("Error: ")
            rospy.loginfo(error)
            rospy.loginfo("------------------------------")
            '''
            rospy.loginfo("------------------------------")
            rospy.loginfo("El índice es: ")
            rospy.loginfo(index)
            rospy.loginfo("Error: ")
            rospy.loginfo(error)
            rospy.loginfo("Consigna X,Y: ")
            rospy.loginfo(X[index])
            rospy.loginfo(Y[index])
            rospy.loginfo("Posicion x,y: ")
            rospy.loginfo(x)
            rospy.loginfo(y)
            rospy.loginfo("------------------------------")
            rospy.sleep(3)

            if(error<=0.3):
                t1 = rospy.Time.now().to_sec()
                '''
                V = 0
                W = 0
                rospy.sleep(6)
                '''
                V = Xd[index]*cos(yaw)+Yd[index]*sin(yaw)
                W = -Xd[index]*sin(yaw)/l+Yd[index]*cos(yaw)/l
                index = index+1
                    
                '''
                if (abs(V)>V_max):
                    V = V_max*abs(V)/V
                    print("Sat V\t")
                if (abs(W)>W_max):
                    W = W_max*abs(W)/W
                    print("Sat W\t")
                '''
                
        else:
            V = 0
            W = 0       
            

    def start(self):
        global X,Y,delta_t,Xd,Yd,t
        rospy.Subscriber("/gazebo/model_states", ModelStates, self.odom_callback)
        t = np.linspace(0, 2*pi, ptos)
        
        #####################
        #Trayectoria circular
        #####################

        Cx = -1.5; Cy = 0
        r = 1.5
        for i in t:
            X.append(Cx + r*cos(i))
            Y.append(Cy + r*sin(i))
        for i in range(len(t)):
            Xd.append(-r*sin(t[i]))
            Yd.append(r*cos(t[i]))


        #######################
        #Trayectoria lemniscata
        #######################
        '''
        alpha = 1.50
        X0 = 2; Y0 = 2.5
        #Coordenadas lemniscata centrada
        for i in t:
            Xsr.append(alpha*sqrt(2)*cos(i) / ((sin(i))**2+1))
            Ysr.append(alpha*sqrt(2)*cos(i)*sin(i) / (sin(i)**2+1))
        #Coordenadas lemniscata rotada y desplazada
        for i in range(len(X)):
            X.append(X0 + X[i]*cos(3*pi/4) + Y[i]*sin(3*pi/4))
            Y.append(Y0 - X[i]*sin(3*pi/4) + Y[i]*cos(3*pi/4))
        for i in range(1,len(X)):
            Xd.append((X[i]-X[i-1])/delta_t)
            Yd.append((Y[i]-Y[i-1])/delta_t)
        '''

        self.rate.sleep()
        rospy.spin()



if __name__ == '__main__':
    rospy.init_node('joy_walle')
    teleop1=teleop_walle()

    try:
        rospy.Timer(rospy.Duration(delta_t), teleop1.start())
        #if(rospy.is_shutdown()):
            #ax.set_aspect('equal', 'box')
            #ax.plot(t, Vel)
            #plt.show()
    except rospy.ROSInterruptException:
        pass
