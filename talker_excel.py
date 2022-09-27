#!/usr/bin/env python3

import rospy
import pandas as pd
from std_msgs.msg import Float32
from random import randint


def time_pub():
    global df
    pub = rospy.Publisher('Tiempo', Float32, queue_size=1000)
    rospy.init_node('time_pub_node', anonymous = True)
    rate = rospy.Rate(3)

    while not rospy.is_shutdown():
        var = float(randint(0,4))
        rospy.loginfo(var)
        pub.publish(var)
        df = df.append({'Tiempo': var}, ignore_index=True)
        rate.sleep()

df = pd.DataFrame(columns = ['Tiempo'])

if __name__ == '__main__':
    try:
        time_pub()
        if rospy.is_shutdown():
            df.to_excel('pandas_to_excel.xlsx', sheet_name = 'Nueva hoja') 
    except rospy.ROSInterruptException:
        pass
