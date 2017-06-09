#-*-coding:UTF-8-*-
'''
Created on 2017年5月25日-下午3:17:35
author: Gary-W
'''
import cv2
import numpy as np
from vpose import VPose
from draw_map import PosMapOld
import config_parser as cfg_parser
import os

class CarModel:
    def __init__(self):
        self.img = cv2.imread("materials/car.png")
        self.img = cv2.resize(self.img, (48,48))
        self.rows = self.img.shape[0]
        self.cols = self.img.shape[1]
        
    def rotate(self, yaw_deg):
        M = cv2.getRotationMatrix2D((self.cols/2,self.rows/2), - yaw_deg,1)
        dst = cv2.warpAffine(self.img,M,(self.cols,self.rows))
        return dst
        
    
class PosMap:
    def __init__(self):
        config_path = r"runtime_setting.txt"
        cfgpar = cfg_parser.TextParser()
        cfg_table = cfgpar(config_path)
        self.map_path = r"materials/%s" % (cfg_table["map_path"])
        self.im_map = cv2.imread(self.map_path)
        h,w,_ = self.im_map.shape
        self.im_h = h
        self.car = CarModel()
        self.mark_layer = np.zeros(self.im_map.shape, np.uint8)
#         self.disp_layer = np.copy(self.im_map)

        self.line_h = 20
        self.disp_layer = np.zeros((h+self.line_h,w,3), np.uint8)
        self.disp_layer[:self.im_h,:,:] = self.im_map[:]
        self.cmd_line = self.disp_layer[h:,:,:]
        
    def mark_vpose(self, x,y,deg):
        im_car = self.car.rotate(deg)
        h,w,_ = im_car.shape
        sub_roi = self.mark_layer[y-h/2:y+h/2, x-w/2:x+w/2,:]
        sub_roi[im_car!=0] = im_car[im_car!=0]
        return self.mark_layer
    
    def mark_vpose_arr(self, vpose_arr):
        self.mark_layer[:] = 0
        for vp in vpose_arr:
            self.mark_vpose(vp.x,vp.y,vp.deg)
        
        self.disp_layer[:self.im_h,:,:] = self.im_map + self.mark_layer
    
    def mark_cmd_text(self,s="123"):
        self.cmd_line[:] = 0
        cv2.putText(self.cmd_line, s, (10,10),
                    cv2.FONT_HERSHEY_PLAIN, 1, (67,197,67), thickness = 1,)


def anime_check_pose(log_path, cfg_table):
    """ 用动画检查生成的pos文件的正确性，用小车画在上面
    """
    pos_map = PosMapOld(cfg_table)
    pose_offset = cfg_table["world_center_offset"]
    with open(log_path,"r") as f:
        headers = f.readline()
        lines = f.readlines()
        for line in lines:
            items = line.strip("\n")
            items = line.split(",")
            frameID = int(items[0])
#             if frameID % 20 != 0: continue
            items = items[1].split(" ")
            x = float(items[0]) + pose_offset[0]
            y = float(items[1]) + pose_offset[1]
            yaw = float(items[2])
            yaw = np.rad2deg(yaw)
            print(frameID, x, y, yaw)
            map_img = pos_map.project_position(x, y, yaw)
            bev_path = r"%s\%06d.jpg" % (cfg_table["bev_root"],frameID)
            if os.path.exists(bev_path):
                im_bev = cv2.imread(bev_path)
                cv2.imshow("result", map_img)
                cv2.imshow("bev", im_bev)
            key = cv2.waitKey(20)
            if key == 32:
                
                key = cv2.waitKey(10)
                while key != 32: 
                    key = cv2.waitKey(10)
    cv2.waitKey(0)
    
def recover_index(log_path, cfg_table):
    pos_map = PosMapOld(cfg_table)
    pose_offset = cfg_table["world_center_offset"]
    with open(log_path,"r") as f:
        headers = f.readline()
        lines = f.readlines()
        for line in lines:
            items = line.strip("\n")
            items = line.split(",")
            frameID = int(items[0])
            items = items[1].split(" ")
            x = float(items[0]) + pose_offset[0]
            y = float(items[1]) + pose_offset[1]
            yaw = float(items[2])
            yaw = np.rad2deg(yaw)
            pos_map.map_img = pos_map.mark_position(x, y, 0)
        pos_map.disp_map()
        
if __name__=="__main__":
    pass

