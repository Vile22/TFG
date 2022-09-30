#!/usr/bin/env python3

import rospy 
from sensor_msgs.msg import JointState

def callback(data):
    rospy.loginfo(rospy.get_name() + ": I heard %s" % data.header.stamp)

def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('pozyx_coords', JointState, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()