#-*-coding:UTF-8-*-
'''
Created on 2017年8月14日-下午3:26:59
author: Gary-W
'''

import config_parser as cfg_parser
import cv2
import os
import numpy as np
from plot_pose import read_can_log
from dataio import get_filelist
from vehicle_model import CanMatchLog,VehicleMotion
from config_parser import TextParser
from draw_map import PosMap

class KeyPoint:
    def __init__(self, log = None):
        self.frame = 0
        self.x = 0
        self.y = 0
        self.yaw_deg = 0

        if log!=None:
            sitem = log.strip().split(" ")
            self.frame = int(sitem[0])
            self.x = float(sitem[1])
            self.y = float(sitem[2])
            self.yaw_deg = float(sitem[3])
            
    def __str__(self):
        return "%05d\tx: %3.5f\ty: %3.5f\tdeg: %3.5f" % (self.frame, self.x, self.y, self.yaw_rad)
            

def getKeyframeTable(gt_file_list):
    keypoint_table = {}
    for path in gt_file_list:
        with open(path,"r") as f:
            slog = f.readline()
            kp = KeyPoint(slog)
            keypoint_table[kp.frame] = kp

    return keypoint_table

class LocDR:
    
    def __init__(self):
        config_path = r"config.txt"
        cfgpar = cfg_parser.TextParser()
        cfg_table = cfgpar(config_path)
        self.vm = VehicleMotion(cfg_table["wheel_base"],cfg_table["vehicle_width"])
        self.bev_root = cfg_table["bev_root"]
        self.can_match_path = cfg_table["can_match_path"]
        self.can_dir = os.path.split(self.can_match_path)[0]
        self.img_filename = self.can_dir + r"\pose_map.jpg"
        self.can_match_logs = read_can_log(self.can_match_path)

        self.keypoint_table = {}

        self.mapper = PosMap()

        self.start_point = []
        self.stop = 0
        self.start = 0
        self.keys = []
        
        self.vhcl_can_data_buffer = []

        self.vm_pose = []

    def add_keypoint(self, key_point):
        self.keypoint_table[key_point.frame] = key_point
        self.keys.append(key_point.frame)
        self.stop = key_point.frame + 1

        if len(self.vm_pose) > 0:
            self.vm_pose.pop()
            self.vm_pose.append((key_point.x, key_point.y, key_point.yaw_deg))
        
        if len(self.start_point)==0:
            self.start = key_point.frame
            print "self.start",self.start
            self.start_point = [key_point.x, key_point.y, key_point.yaw_deg]
            self.vm.setPosition(self.start_point[0],self.start_point[1],self.start_point[2])
            self.vm_pose.append((key_point.x, key_point.y, key_point.yaw_deg))
            self.vhcl_can_data_buffer.append(self.can_match_logs[key_point.frame])
    
    def pop(self, frameID):
        if len(self.vm_pose) > 0:
            self.vm_pose.pop()
        if len(self.vhcl_can_data_buffer) > 0:
            self.vhcl_can_data_buffer.pop()
        
        if frameID in self.keys:
            self.keys.pop()
            self.keypoint_table.pop(frameID)
        
        if len(self.keys) == 0:
            self.start_point = []
            
    
    def updateDR(self, frameID):
        if len(self.start_point) == 0:
            return
        vhcl_can_data = self.can_match_logs[frameID]
        times = vhcl_can_data.data["time_stamp"] - self.vhcl_can_data_buffer[-1].data["time_stamp"]
        print times
        
        
        vm_last = self.vm_pose[-1]
        
        self.vm.setPosition(vm_last[0], vm_last[1], vm_last[2])

        self.vm.traject_predict_world(vhcl_can_data, times)
        
        self.vm_pose.append((self.vm.pos.x, self.vm.pos.y, np.rad2deg(self.vm.theta)))
        
        self.vhcl_can_data_buffer.append(vhcl_can_data)

        print self.vm.pos.x, self.vm.pos.y, self.vm.theta
        
    
    
    def update_trace(self):
        for pos in self.vm_pose:
            pos_x, pos_y, pos_yaw = pos
            self.mapper.mark_position(pos_x, pos_y, pos_yaw, False)

#         self.mapper.disp_map()



if __name__=="__main__":
    pass
    loc_dr = LocDR()
    gt_file_list = get_filelist(r"D:\bev\7x7_(-1--1)", ".txt")
    gttable = getKeyframeTable(gt_file_list)
    loc_dr.keypoint_table = gttable
    loc_dr.keys = sorted(loc_dr.keypoint_table.keys())
    st = loc_dr.keys[0]
    loc_dr.start_point = [loc_dr.keypoint_table[st].x,
                        loc_dr.keypoint_table[st].y,
                        loc_dr.keypoint_table[st].yaw_deg]
    
    loc_dr.start = 1001
    loc_dr.stop = 1500
    
    vm_pose = loc_dr.insertDR()
    loc_dr.disp_pose(vm_pose)
    
    
    