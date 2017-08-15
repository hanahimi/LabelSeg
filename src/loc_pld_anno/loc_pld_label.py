#-*-coding:UTF-8-*-
'''
Created on 2017年8月10日-下午6:30:54
author: Gary-W

基于PLD与库位匹配的定位标注工具（手动）
1 按下数字（1,2,3,4）
2 点击对应像素
3 按下另一数字（1,2,3,4）
4 点击对应像素
5 输入库位号（eg。 B01） 回车
6 显示车在地图上的投影，每个图像保存一个txt
7 按空格下一幅
'''

import config_parser as cfg_parser
import cv2
import os
from loc_plam import *
from pld_map import *
from draw_map import *
from dataio import get_filelist
from keyframe_insert import *


class LocPldLabeler:

    def __init__(self):
        self.win_title = "loc labeler"
        config_path = r"config.txt"
        cfgpar = cfg_parser.TextParser()
        cfg_table = cfgpar(config_path)
        
        self.bev_root = cfg_table["bev_root"]
        self.gt_root = cfg_table["gt_root"]
        
        self.pix_w = cfg_table["pix_w"]
        self.pix_h = cfg_table["pix_h"]
        self.save = 1 if (cfg_table["save"]=="on") else 0
        
        self.bev_disp_w = 512
        self.bev_disp_h = 512
        
        self.car_center_x_ori = cfg_table["car_center_x"]
        self.car_center_y_ori = cfg_table["car_center_y"]
        
        self.car_center = (self.car_center_x_ori * self.bev_disp_w/384,
                           self.car_center_y_ori * self.bev_disp_w/384) # imgx, imgy 

        self.imlist = get_filelist(self.bev_root, ".jpg")
        self.img_num = len(self.imlist)
        self.img_idx = 0
        _cur_img = cv2.imread(self.imlist[self.img_idx])
        self.cur_img = cv2.resize(_cur_img, (512,512))
        
        cv2.namedWindow(self.win_title)
        cv2.setMouseCallback(self.win_title,self.mouse_add_point)
        
        self.pixs = []
        self.pld_pose = []
        
        self.point_id = 0

        # 载入车位数据库
        self.pklb = ParkLibrary("parklot_corrid.txt")

        self.plam = PkPlam(self.bev_disp_w, 0)
        
        # 载入地库地图
        self.pm = PosMap()

        
        # 全局面板
        self.window = np.zeros((max(self.bev_disp_h, self.plam.h, self.pm.h),
                                self.bev_disp_w+self.plam.w+self.pm.w, 3), np.uint8)
        self.win_H = self.window.shape[0]
        self.win_W = self.window.shape[1]

        self.sub_window = np.zeros((80,80,3), np.uint8)
        
        self.console_output = ""
        self.update_console("All Setting Loaded")
        
        
    def mouse_add_point(self,event, x, y,flags,param):
        """
        当按下左键在画面标注一个角点, 标注该角点在车辆坐标系下的位置
        当第二次按下时，计算车辆在世界坐标系下的位置
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            # 检测鼠标 角点区域
            if (0 < x < self.bev_disp_w) and (0 < y < self.bev_disp_h):
                if len(self.pixs) < 2:
                    addCorner(self.cur_img,x,y,self.point_id+1)
                    self.pixs.append((self.point_id, x,y))
                    
                    pldx = (x - self.car_center[0])/self.pix_w
                    pldy = (self.car_center[1] - y)/self.pix_h
                    self.pld_pose.append((self.point_id, pldx, pldy))
                    addCorrid(self.cur_img,x,y,pldx,pldy)
                    
#                     self.point_id += 3
            
            # 检测鼠标 按钮区域
            if (self.bev_disp_w < x < self.bev_disp_w+self.plam.w) and (0 < y < self.win_H):
                strKey =  self.plam.getKey(x, y)
                if strKey != 0:
                    if strKey == "Enter":
                        if len(self.pld_pose)==2:
                            if len(self.plam.key_log) > 0:
                                pk_id_str = "".join(self.plam.key_log)
                                if pk_id_str in self.pklb.park_table:
                                    theta_deg, x_car, y_car = self.pklb.calcVehWorldPosion(self.pld_pose, pk_id_str)
                                    self.pm.project_position(x_car, y_car, theta_deg)

                                    if self.save == 1:
                                        self.save_labeling(x_car, y_car, theta_deg)
                                    self.update_console("sav Wx:%2.2fm Wy:%2.2fm H:%2.2fdeg" % (x_car,y_car, theta_deg))
                                else:
                                    self.update_console("invalid input")
                            else:
                                self.update_console("no pk num")
                        else:
                            self.update_console("no corner point")

                    elif strKey == "Clear":
                        self.plam.clear()
                    else:
                        self.plam.key_log.append(strKey)
                        self.plam.updateDisplayer()

        if event == cv2.EVENT_MOUSEMOVE:
            self.update_console("x : %d y : %d" % (x,y), pos = 2)
            self.update_subWindow(x, y)
            
    def keyboard_respond(self, key):
        """ 响应键盘事件
        """
        if key==114:    # R
            impath = self.imlist[self.img_idx]
            imname = os.path.split(impath)[-1][:-4]
            gtpath = impath[:-3]+"txt"
            gtpath = "%s/%s" % (self.gt_root, imname+".txt")
            if os.path.exists(gtpath):
                os.remove(gtpath)
            
        if key==27:
            print("esc")
            return 0
        
        """
        每次切换帧时，应执行一次运动模型的推算，从上一帧开始 推算当前帧
        并在地图中画出车的路径
        """
        if key==97:         # "A"
            self.point_id = 0
            self.pixs = []
            self.pld_pose = []
            if (self.img_idx >0):
                self.point_num = 0
                self.img_idx -= 1
            _cur_img = cv2.imread(self.imlist[self.img_idx])
            
            imname = os.path.split(self.imlist[self.img_idx])[-1][:-4]
            
            self.cur_img = cv2.resize(_cur_img, (512,512))
            self.update_console("load id: %s" % imname)
            
        if key==100:        # "D"
            self.point_id = 0
            self.pixs = []
            self.pld_pose = []
            if (self.img_idx<self.img_num-1):
                self.point_num = 0
                self.img_idx += 1
            _cur_img = cv2.imread(self.imlist[self.img_idx])
            self.cur_img = cv2.resize(_cur_img, (512,512))
            imname = os.path.split(self.imlist[self.img_idx])[-1][:-4]
            self.update_console("load id: %s" % imname)


        if key==97 or key==100:
            impath = self.imlist[self.img_idx]
            imname = os.path.split(impath)[-1][:-4]
            gtpath = impath[:-3]+"txt"
            gtpath = "%s/%s" % (self.gt_root, imname+".txt")
 
            if os.path.exists(gtpath):
                with open(gtpath,"r") as f:
                    l = f.readline()
                    items = l.strip().split(" ")  
                    _, x_car, y_car, theta_deg = [float(a) for a in items]
                    self.pm.project_position(x_car, y_car, theta_deg)
            else:
                self.pm.result[:] = self.pm.map_img

        if key==32:
            print "space"
            
        # 1,2,3,4
        if key==49:
            self.update_console("sel point 1")
            self.point_id = 0
        if key==50:
            self.update_console("sel point 2")
            self.point_id = 1
        if key==51:
            self.update_console("sel point 3")
            self.point_id = 2
        if key==52:
            self.update_console("sel point 4")
            self.point_id = 3
    
    def save_labeling(self,x_car, y_car, theta_deg):
        impath = self.imlist[self.img_idx]
        imname = os.path.split(impath)[-1][:-4]
        gtpath = "%s/%s" % (self.gt_root, imname+".txt")
        with open(gtpath,"w") as f:
            # frameID, Wx, Wy, Wtheta-deg
            gt = "%s %3.5f %3.5f %3.5f" % (imname, x_car, y_car, theta_deg)
            f.write(gt)
        
    def update_subWindow(self, x, y):
        sh,sw,_ = self.sub_window.shape
        if y-sh/4 < 0 or y+sh/4 > self.bev_disp_h-1\
            or x-sw/4 < 0 or x+sw/4 > self.bev_disp_w-1:
            return
        im = self.window[y-sh/4:y+sh/4,x-sw/4:x+sw/4]
        self.sub_window = cv2.resize(im, (sw,sh))
        cv2.line(self.sub_window, (sw/2,0),(sw/2,y-1), (100,200,100),1)
        cv2.line(self.sub_window, (0,sh/2),(sw-1,sh/2), (100,200,100),1)
        
        sx = 700
        sy = 400
        self.window[sy:sy+sh, sx:sx+sw][:] = self.sub_window[:]
        
    def update_console(self, str_input, pos = 1):
        if pos == 1:    # 更新debug提示
            self.window[348:398,531:854,:] = 0
            cv2.putText(self.window, str_input, (531,358),cv2.FONT_HERSHEY_DUPLEX, 0.5,(200,200,200),thickness=1)

        elif pos == 2: # 更新上方过程参数
            self.window[480:510,525:680,:] = 0
            cv2.putText(self.window, str_input, (526,503),cv2.FONT_HERSHEY_PLAIN, 0.8,(200,200,100),thickness=1)

    def mainloop(self):
        """ 所有控件的主循环
        """
        while (1):
            self.window[:self.bev_disp_h, :self.bev_disp_w,:] = self.cur_img[:]
            self.window[:self.plam.h, self.bev_disp_w:self.bev_disp_w+self.plam.w,:] = self.plam.bg[:]
            self.window[:self.pm.h, self.bev_disp_w+self.plam.w:self.bev_disp_w+self.plam.w+self.pm.w,:] = self.pm.result[:]
            
            cv2.imshow(self.win_title, self.window)
            key = cv2.waitKey(10) & 0xFF
            if 0 == self.keyboard_respond(key):
                break
    
        
if __name__=="__main__":
    pass
    pm = LocPldLabeler()
    pm.mainloop()


