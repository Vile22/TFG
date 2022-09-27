#!/usr/bin/env python

import rospy
import pandas as pd
import openpyxl
from std_msgs.msg import Float32


def callback(data):
    global df
    rospy.loginfo(rospy.get_caller_id() + "I heard %f", data.data)
    df = df.append({'Tiempo': data.data}, ignore_index=True)

def time_sub():
    rospy.init_node('time_sub_node', anonymous = True)
    rospy.Subscriber('Tiempo', Float32, callback)
    rospy.spin()

df = pd.DataFrame(columns = ['Tiempo'])

if __name__ == '__main__':
    time_sub(df)

    if rospy.is_shutdown():
        df.to_excel('pandas_to_excel.xlsx', sheet_name = 'Nueva hoja') 
