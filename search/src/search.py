#! /usr/bin/python
# -*- coding: utf-8 -*-

import os, time
import rospy
from geometry_msgs.msg import PointStamped
from servos.msg import XYPose
from std_msgs.msg import Empty, String

class Search():
    def __init__(self):
        rospy.init_node('search')
        self.servos_pub = rospy.Publisher('/servos_pose', XYPose, queue_size=1)
        self.search_feedback_pub = rospy.Publisher('/search_feedback', String, queue_size=1)
        rospy.Subscriber('/aruco_single/pixel', PointStamped, self.aruco_update)
        rospy.Subscriber('/search_start', Empty, self.start_search)
        rospy.Subscriber('/search_cancel', Empty, self.clear_search)

        self.servos_pose = XYPose()
        self.rate = rospy.Rate(5)
        
    def aruco_update(self, msg):
        self.aruco_pixel = msg

    def clear_search(self, msg=None):
        time_breakpoint = time.time()
        self.is_search = False
        self.servos_pose.x, self.servos_pose.y = 10, 10
        self.servos_pub.publish(self.servos_pose)
        while time.time() - time_breakpoint < 2:
            pass
        self.aruco_pixel = PointStamped()

    def start_search(self, msg):
        self.clear_search()
        self.is_search = True
        while self.is_search:
            if self.aruco_pixel.point.x:
                #rospy.loginfo("pixel: x {}, y {}".format(self.aruco_pixel.point.x, self.aruco_pixel.point.y))
                if self.aruco_pixel.point.x > 320:
                    self.servos_pose.x += 1
                else:
                    self.servos_pose.x -= 1

                if self.aruco_pixel.point.y < 240:
                    self.servos_pose.y += 1
                else:
                    self.servos_pose.y -= 1

                if 310 < self.aruco_pixel.point.x < 330 and 230 < self.aruco_pixel.point.y < 250:
                    self.search_feedback_pub.publish("Наведение выполнено")
                    break
            else:
                self.servos_pose.x += 1
            #rospy.loginfo(self.servos_pose.x)
            if not (0 < self.servos_pose.x < 100 and 0 < self.servos_pose.y < 100):
                if self.aruco_pixel.point.x:
                    self.search_feedback_pub.publish("Цель потеряна")
                else:
                    self.search_feedback_pub.publish("Цель не найдена")
                self.clear_search()
                break

            self.servos_pub.publish(self.servos_pose)
            self.rate.sleep()

if __name__ == "__main__":
    Search()
    rospy.spin()
