#!/usr/bin/env python3
import rospy
import csv
from geometry_msgs.msg import Point32, Point, Pose

# Global vars
csv_writer = None

def scan_callback(msg):
    d = msg.ranges [90]
    if csv_writer is not None:
        csv_writer.writerow(d)

def main():
    rospy.init_node("pozyx_csv")
    sub = rospy.Subscriber('/pozyx_pose',Pose, scan_callback)
    fh = open("\\1.csv", "wb")
    csv_writer = csv.writer(fh) # More constant params
    rospy.spin()
    fh.close()
    csv_writer = None

if __name__ == '__main__':
    main()
