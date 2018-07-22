#! /usr/bin/python

import rospy
from servos.msg import XYPose

def mouse_pose(msg):
    pose.x = msg.x
    pose.y = msg.y

if __name__ == '__main__':
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('/servos_pose', XYPose, queue_size=1)
    rospy.Subscriber('/mouse_pose', XYPose, mouse_pose)

    pose = XYPose()
    pose.x = 0
    pose.y = 0
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        pub.publish(pose)
        rate.sleep()