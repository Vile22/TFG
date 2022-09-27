#!/usr/bin/python3

import rospy
import pandas as pd
import openpyxl
from std_msgs.msg import Float64

df = pd.DataFrame(columns = ['Tiempo'])

def callback(data):
	rospy.loginfo(rospy.get_caller_id() + "I heard %lf", data.data)
	df = df.append({'Tiempo': data.data}, ignore_index=True)

def time_sub():
	rospy.init_node('time_sub_node', anonymous = True)
	rospy.Subscriber('Time', Float64, callback)
	rospy.spin()

if __name__ == '__main__':
	try:
		time_sub()
	except rospy.ROSInterruptException:
		df.to_excel('pandas_to_excel.xlsx', sheet_name = 'Nueva hoja')
