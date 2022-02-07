#!/usr/bin/env python3

import sys
import cv2
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import rospy
import os

class ros_usb_cam:
    def __init__(self,image_store_location):
        
        self.img_sub= rospy.Subscriber("csi_img",Image, self.callback)
        self.cvbridge= CvBridge()
        self.image_count=1
        self.image_store_location= image_store_location

    def callback(self,data):
        print("image {num} received" .format(num=self.image_count))
        
        cv_image=self.cvbridge.imgmsg_to_cv2(data,"bgr8")
        file_name="{loc}/image{count}.jpeg" .format(loc=self.image_store_location,count=self.image_count)
        self.image_count=self.image_count+1
        
        cv2.imwrite(file_name,cv_image)

if __name__=="__main__":
    if(len(sys.argv))!=3:
        print("please provide values for node_name, topic_name, image_store_location in same order")
    else:
        print("starting node with node name={name},image location={loc}" .format(name=sys.argv[1],loc=sys.argv[2]))
        rospy.init_node(sys.argv[1],anonymous=True)
        obj=ros_usb_cam(sys.argv[2])
        try:
            rospy.spin()
        except KeyboardInterrupt:
            print("stopping the node")
                

