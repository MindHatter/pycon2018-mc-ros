#! /usr/bin/python

import rospy
from servos.msg import XYPose
import Tkinter as tk

def correct(coor):
    return 0 if coor <= MAX else MAX

def motion(event):
    pose.x = event.x//2 if 0 <= event.x <= MAX*2 else correct(event.x)
    pose.y = event.y//2 if 0 <= event.y <= MAX*2 else correct(event.y)
    coor.config(text="x: {} y: {}".format(pose.x, pose.y))
    pub.publish(pose)

if __name__ == "__main__":
    MAX = 80

    root = tk.Tk()
    root.geometry('160x160')
    coor = tk.Label(root)
    coor.pack(fill="both", expand=True)

    rospy.init_node("mouse_control")
    pub = rospy.Publisher("/mouse_pose", XYPose, queue_size=1)
    pose = XYPose()
    root.bind('<B1-Motion>', motion)
    root.mainloop()
