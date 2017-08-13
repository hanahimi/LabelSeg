#-*-coding:UTF-8-*-
'''
Created on 2017��8��10��-����10:10:42
author: Gary-W
'''

import cv2
import numpy as np
from dataio import get_filelist


class Point:
    def __init__(self):
        # ϵͳ��������ϵ (cm)
        self.x = None
        self.y = None
    def __str__(self):
            return "x: "+str(self.x)+" y: "+str(self.y)

class Parking:
    """
    �ǵ�����������ļ���
    ȡ����ߵ������˵���Ϊ���1���յ�4����˳ʱ�뷽��������������ͣ��λ����״1,2,3,4
    """
    def __init__(self, csv_log=None):
        self.name = None
        # �ǵ�����(1,2,3,4) ��Ӧ���� 0,1,2,3
        self.corner = [Point() for i in range(4)]

        if csv_log != None:
            self.name = csv_log[0]
            for i in range(4):
                self.corner[i].x = float(csv_log[1+i*2])
                self.corner[i].y = float(csv_log[2+i*2])

    def __str__(self):
        s = "\n".join([self.name + (" %d: "% (i+1)) + self.corner[i].__str__() for i in range(4)])
        return s

class ParkLibrary:
    def __init__(self, pk_path):
        self.park_table = {}
        
        with open(pk_path, "r") as f:
            f.readline()
            lines = f.readlines()
            for line in lines:
                pk_log = line.strip("\n").split(" ")
                pk = Parking(pk_log)
                self.park_table[pk.name] = pk
    
    def getPk(self,name):
        return self.park_table[name]


    def calcVehWorldPosion(self, pld_pose, name):
        """ ���㳵������������ϵλ�úͽǶ�
        """
        pk = self.getPk(name)
        id1,car_x1,car_y1 = pld_pose[0]
        id2,car_x2,car_y2 = pld_pose[1]
        world_x1,world_y1 = pk.corner[id1].x, pk.corner[id1].y
        world_x2,world_y2 = pk.corner[id2].x, pk.corner[id2].y
        v_car = (car_x1 - car_x2, car_y1 - car_y2) 
        v_world = (world_x1 - world_x2, world_y1 - world_y2) 
        a = v_car[0]*v_world[0] + v_car[1]*v_world[1]
        v_c_m = np.sqrt(v_car[0]**2 + v_car[1]**2)
        v_w_m = np.sqrt(v_world[0]**2 + v_world[1]**2)
        theta = np.arccos(1.0*a / (v_c_m*v_w_m))
        x_car = world_x1 - (np.cos(theta)*car_x1 - np.sin(theta)*car_y1)
        y_car = world_y1 - (np.sin(theta)*car_x1 + np.cos(theta)*car_y1)
        return np.rad2deg(theta), x_car, y_car
        
def addCorner(src_img,x,y,_id):
    l = 2
    cv2.line(src_img, (x,y),(x+l,y), (200,200,100),1)
    cv2.line(src_img, (x,y),(x-l,y), (200,200,100),1)
    cv2.line(src_img, (x,y),(x,y+l), (200,200,100),1)
    cv2.line(src_img, (x,y),(x,y-l), (200,200,100),1)
    cv2.putText(src_img, "%d"%_id, (x+5,y), cv2.FONT_HERSHEY_PLAIN, 1.0,(200,200,100),thickness=1)

def addCorrid(src_img,x,y,pldx,pldy):
    cv2.putText(src_img, "rX: %2.3f" % pldx, (x+20,y-6), cv2.FONT_HERSHEY_PLAIN, 0.8,(200,200,100),thickness=1)
    cv2.putText(src_img, "rY: %2.3f" % pldy, (x+20,y+6), cv2.FONT_HERSHEY_PLAIN, 0.8,(200,200,100),thickness=1)

    
    


if __name__=="__main__":
    pass

