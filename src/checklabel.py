#-*-coding:UTF-8-*-
'''
Created on 2017年3月6日-上午11:28:45
author: Gary-W
'''

import cv2
import numpy as np
import os
from config_parser import TextParser
parser = TextParser()
text_path = r"config.txt"
  
text_path = r"config.txt"
items_table = parser(text_path)

img_path = items_table["img_path"]
img_path = img_path[:-4]+"_seq.png"
img_seg = cv2.imread(img_path)[:,:,0 ]

imgshow = img_seg * 25

cv2.imshow("label", imgshow)
cv2.waitKey(0)

if __name__=="__main__":
    pass

