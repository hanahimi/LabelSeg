#-*-coding:UTF-8-*-
'''
Created on 2017年1月12日-下午3:30:08
author: Gary-W

地图绘制，坐标点投影
'''
import cv2
import numpy as np

class CarModel:
    def __init__(self):
        self.img = cv2.imread(r'car.png')
        self.img = cv2.resize(self.img, (48,48))
        self.rows = self.img.shape[0]
        self.cols = self.img.shape[1]
        
    def get_rot(self, yaw_deg):
        M = cv2.getRotationMatrix2D((self.cols/2,self.rows/2), - yaw_deg,1)
        dst = cv2.warpAffine(self.img,M,(self.cols,self.rows))
        return dst

class PosMap:
    """ 地图绘制类
    用于将世界坐标映射到图片上，可以使用配置文件进行参数设置
    attribute:
      map_img: 原始地图数据
      coef: 坐标投影参数
    """
    def __init__(self):
        self.map_path = r"map.jpg"
        self.map_img = cv2.imread(self.map_path)

        self.mark_result = cv2.imread(self.map_path)

        self.h = self.map_img.shape[0]
        self.w = self.map_img.shape[1]
        
        self.coef = [42,413, 7, -7]
        self.car_logo = CarModel()
        self.result = np.copy(self.map_img)
        
    def project_position(self, pos_x, pos_y, pos_yaw):
        """ 将世界坐标系的点记录到图像中，画上小车
            当原有的图像发生过改变时，读入新的图像
        input:
          pos_x, pos_y, pos_yaw(deg)
        """
        self.result = np.copy(self.map_img)

        car_img = self.car_logo.get_rot(pos_yaw)
        h,w,_ = car_img.shape
        pil_x = int(1.0 * pos_x * self.coef[2] + self.coef[0])
        pil_y = int(1.0 * pos_y * self.coef[3] + self.coef[1])
        sub_roi = self.result[pil_y-h/2:pil_y+h/2, pil_x-w/2:pil_x+w/2,:]
        sub_roi[car_img!=0] = car_img[car_img!=0]

    def mark_position(self, pos_x, pos_y, pos_yaw, keypoint=False):
        """ 将世界坐标系的点记录到图像中，改写原有图像
        input:
          pos_x, pos_y, pos_yaw
        output:
          map_img: 系统图像的当前状态
        """
        pil_x = int(1.0 * pos_x * self.coef[2] + self.coef[0])
        pil_y = int(1.0 * pos_y * self.coef[3] + self.coef[1])
        
        if keypoint:
            cv2.circle(self.mark_result,(pil_x,pil_y),5,(0,0,255),-1)
        else:
            cv2.circle(self.mark_result,(pil_x,pil_y),9,(19,162,247),1)
            cv2.circle(self.mark_result,(pil_x,pil_y),2,(0,0,0),-1)
        self.ischanged = True

        return self.map_img
    
    def disp_map(self, filename=None):
        h,w,_ = self.map_img.shape
        imresize = cv2.resize(self.map_img, (w*2/3, h*2/3))
        cv2.imshow("map",imresize)
        if filename:
            cv2.imwrite(filename,imresize)
        cv2.waitKey(0)
        
        
if __name__=="__main__":
    pass
    pm = PosMap()
    pm.project_position(0,0,0)
    cv2.imshow("ss", pm.result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    