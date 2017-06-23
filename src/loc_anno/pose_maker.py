#-*-coding:UTF-8-*-
'''
Created on 2017年5月25日-下午3:02:03
author: Gary-W
'''
import cv2
from vpose import VPose, save_vpose_arr
from render import PosMap
from cmd_parse import CommandParser
import os

import config_parser as cfg_parser

class PoseMaker:
    
    def __init__(self):
        self.win_title = "Pose_Maker"
        self.pos_map = PosMap()
        self.cmdp = CommandParser()
        config_path = r"runtime_setting.txt"
        cfgpar = cfg_parser.TextParser()
        cfg_table = cfgpar(config_path)
        self.cfg_table = cfg_table
        self.bev_root = cfg_table["bev_root"] + "\\" + cfg_table["bev_name"]
        self.mark_filename = cfg_table["bev_root"] + "\\pose_mark.txt"

        self.niter = 10
        self.vpose_arr = []
        self.id_arr = []

        self.r_button = 0
        self.l_button = 0
        self.rot_orient = 1
        self.cur_id = 0
        if cfg_table["recover"] == 1:
            if os.path.exists(self.mark_filename):
                with open(self.mark_filename) as mf:
                    lines = mf.readlines()
                    for line in lines:
                        fid,x,y,deg = line.strip("\n").split(" ")
                        vp = VPose(int(fid), int(x), int(y), float(deg))
                        self.vpose_arr.append(vp)
                        self.id_arr.append(vp.id)
                    if self.vpose_arr:
                        self.cur_id = self.vpose_arr[-1].id



        cv2.namedWindow(self.win_title)
        cv2.setMouseCallback(self.win_title,self.cb_add_position)
        

    def cb_add_position(self,event, x, y,flags,param):
        """
        1. 当按下左键时返回当前位置坐标, 并在队列中添加一个新的位置标记
        2. 当按下右键时位置队列最前端的标记，逆时针旋转一定角度
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            self.l_button = 1
            if self.vpose_arr:
                vp = VPose(self.cur_id,x,y,self.vpose_arr[-1].deg)
            else:
                vp = VPose(self.cur_id,x,y,0)
            if vp.id not in self.id_arr: 
                print("new point is (%d,%d,%2.2f) id=%d" % (vp.x, vp.y, vp.deg,vp.id))
                self.vpose_arr.append(vp)
                self.id_arr.append(vp.id)
                self.pos_map.mark_vpose_arr(self.vpose_arr)
        
        elif event == cv2.EVENT_LBUTTONUP:
            self.l_button = 0
            if self.vpose_arr:
                vp = self.vpose_arr[-1]
            
        elif event == cv2.EVENT_RBUTTONDOWN:
            if self.vpose_arr:
                self.r_button = 1
                
        elif event == cv2.EVENT_RBUTTONUP:
            self.r_button = 0
            if self.vpose_arr:
                vp = self.vpose_arr[-1]
            
                
    def cicle_on_delay(self):
        """ 在主循环中的周期性的循环调用事件
        """
        if self.r_button == 1:
            if self.vpose_arr[-1].id == self.cur_id:
                self.vpose_arr[-1].rotate_clk_wise(
                            d_deg = .5,
                            ori=1)
                self.pos_map.mark_vpose_arr(self.vpose_arr)
                vp = self.vpose_arr[-1]
                self.pos_map.mark_cmd_text("cur id:%d  (%d,%d,%2.2f)-%d" \
                               % (self.cur_id, vp.x, vp.y, vp.deg,vp.id))
        if self.l_button == 1:
            if self.vpose_arr[-1].id == self.cur_id:
                self.vpose_arr[-1].rotate_clk_wise(
                            d_deg = -.5,
                            ori=1)
                self.pos_map.mark_vpose_arr(self.vpose_arr)
                vp = self.vpose_arr[-1]
                self.pos_map.mark_cmd_text("cur id:%d  (%d,%d,%2.2f)-%d" \
                               % (self.cur_id, vp.x, vp.y, vp.deg,vp.id))
        
    def keyboard_respond(self, key):
        """ 响应键盘事件
        """
        if key==27:
            print("esc")
            return 0

        if key==13: # 按Enter保存当前所有标记
            save_vpose_arr(self.mark_filename, self.vpose_arr)
            self.pos_map.mark_cmd_text("cur id:%d  mark saved" % self.cur_id)
        
        if  self.vpose_arr and self.vpose_arr[-1].id == self.cur_id:
            if key==ord('1'): # - 切换逆时针旋转
                self.vpose_arr[-1].rotate_clk_wise(-.1,1)
            elif key==ord('2'): # + 切换顺时针旋转
                self.vpose_arr[-1].rotate_clk_wise(.1,1)
            elif key==ord('a'): # 向左微调单位像素
                self.vpose_arr[-1].x -= 1
            elif key==ord('d'): # 向右微调单位像素
                self.vpose_arr[-1].x += 1
            elif key==ord('w'): # 向上微调单位像素
                self.vpose_arr[-1].y -= 1
            elif key==ord('s'): # 向下微调单位像素
                self.vpose_arr[-1].y += 1
            vp = self.vpose_arr[-1]
#             self.pos_map.mark_cmd_text("cur id:%d  (%d,%d,%2.2f)-%d" \
#                    % (self.cur_id, vp.x, vp.y, vp.deg,vp.id))

            pft = self.cfg_table["project_factors"]
            pose_offset = self.cfg_table["world_center_offset"]
            wx = 1.0*(vp.x - pft[0])/pft[2] - pose_offset[0]
            wy = 1.0*(vp.y - pft[1])/pft[3] - pose_offset[1]

            self.pos_map.mark_cmd_text("cur id:%d  (%d,%d,%2.2f)-%d" \
                   % (self.cur_id, wx, wy, vp.deg,vp.id))


        if key==ord('i'): # 输入命令
            command = raw_input("input cammand:\n")
            res = self.cmdp.trans(command)
            self.cur_id = res
        
        if key==ord('q'): # 后退1帧
            if self.cur_id > 0:
                self.cur_id -= self.niter
                self.pos_map.mark_cmd_text("cur id:%d" % self.cur_id)
        if key==ord('e'): # 前进1帧
            self.cur_id += self.niter
            self.pos_map.mark_cmd_text("cur id:%d" % self.cur_id)
        
        if key==ord('c'): # 清空所有标记
            self.cur_id = 0
            self.vpose_arr = []
            self.id_arr = []
            self.pos_map.mark_cmd_text("cur id:%d clear all marker" % self.cur_id)


        if key==ord('z'): # 清除最近标记
            if self.vpose_arr:
                vp = self.vpose_arr[-1]
                self.vpose_arr.pop()
                self.id_arr.pop()
                self.cur_id = 0
            if self.vpose_arr:
                self.cur_id = self.vpose_arr[-1].id
                self.pos_map.mark_cmd_text("cur id:%d" % self.cur_id)
            else:
                self.pos_map.mark_cmd_text("cur id:%d" % 0)
        
        self.pos_map.mark_vpose_arr(self.vpose_arr)
        return 1
        
    def mainloop(self):
        """
        所有控件的主循环
        """
        while(1):
            cv2.imshow(self.win_title, self.pos_map.disp_layer)
            bev_path = "%s/%06d.jpg" % (self.bev_root,self.cur_id)
            if os.path.exists(bev_path):
                bev = cv2.imread(bev_path)
                cv2.imshow("bev", bev)
            else:
                self.cur_id = 0
            key = cv2.waitKey(10) & 0xFF

            # 调用周期处理
            self.cicle_on_delay()
            # 查找当前帧的键盘响应
            if 0 == self.keyboard_respond(key):
                break

if __name__=="__main__":
    pass
    pm = PoseMaker()
    pm.mainloop()


