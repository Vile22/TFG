#!/usr/bin/python3

import rospy
from std_msgs.msg import Float64


def time_pub():
    pub = rospy.Publisher('Time', Float64, queue_size=100)
    rospy.init_node('time_pub_node', anonymous = True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        time = Float64(rospy.get_time)
        rospy.loginfo(time)
        pub.publish(time)
        rate.sleep()


if __name__ == '__main__':
    try:
        time_pub()
    except rospy.ROSInterruptException:
        pass
