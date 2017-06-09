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
        self.img = cv2.imread(r'materials/car.png')
        self.img = cv2.resize(self.img, (48,48))
        self.rows = self.img.shape[0]
        self.cols = self.img.shape[1]
        
    def get_rot(self, yaw_deg):
        M = cv2.getRotationMatrix2D((self.cols/2,self.rows/2), - yaw_deg,1)
        dst = cv2.warpAffine(self.img,M,(self.cols,self.rows))
        return dst

class PosMapOld:
    """ 地图绘制类
    用于将世界坐标映射到图片上，可以使用配置文件进行参数设置
    attribute:
      map_img: 原始地图数据
      coef: 坐标投影参数
    """
    def __init__(self,config_table):
        self.map_path = r"materials/%s" % (config_table["map_path"])
        self.map_img = cv2.imread(self.map_path)
        self.coef = config_table["project_factors"]
        self.ischanged = False
        self.car_logo = CarModel()
    
    def compare_position(self, gtx, gty, gtyaw, dtx,dty,dtyaw):
        """ 对比GT点的位置(红色) 和 预测点的位置(绿色)
        output:
          map_img: 系统图像的当前状态
        """
        pil_x_gt = int(1.0 * gtx * self.coef[2] + self.coef[0])
        pil_y_gt = int(1.0 * gty * self.coef[3] + self.coef[1])
        cv2.circle(self.map_img,(pil_x_gt,pil_y_gt),2,(117,152,253),-1)
        
        pil_x_dt = int(1.0 * dtx * self.coef[2] + self.coef[0])
        pil_y_dt = int(1.0 * dty * self.coef[3] + self.coef[1])
        cv2.circle(self.map_img,(pil_x_dt,pil_y_dt),2,(244,254,129),-1)
        
        cv2.line(self.map_img,(pil_x_gt,pil_y_gt),(pil_x_dt,pil_y_dt),(233,132,251),1)
        
        return self.map_img
    
    def mark_position(self, pos_x, pos_y, pos_yaw):
        """ 将世界坐标系的点记录到图像中，改写原有图像
        input:
          pos_x, pos_y, pos_yaw
        output:
          map_img: 系统图像的当前状态
        """
#         print pos_x, pos_y 
        pil_x = int(1.0 * pos_x * self.coef[2] + self.coef[0])
        pil_y = int(1.0 * pos_y * self.coef[3] + self.coef[1])
        cv2.circle(self.map_img,(pil_x,pil_y),1,(19,162,247),-1)
        self.ischanged = True

        return self.map_img
    
    def mark_position_id(self, pos_x, pos_y, pos_yaw, _id):
        """ 将世界坐标系的点记录到图像中，改写原有图像
        input:
          pos_x, pos_y, pos_yaw
        output:
          map_img: 系统图像的当前状态
        """
#         print pos_x, pos_y 
        pil_x = int(1.0 * pos_x * self.coef[2] + self.coef[0])
        pil_y = int(1.0 * pos_y * self.coef[3] + self.coef[1])
        cv2.circle(self.map_img,(pil_x,pil_y),1,(19,162,247),-1)
        if _id%100==0:
            cv2.putText(self.map_img, str(_id),(pil_x,pil_y),  
                        cv2.FONT_HERSHEY_PLAIN, 1, (19,24,250), thickness = 1,)
            cv2.circle(self.map_img,(pil_x,pil_y),3,(19,24,24),-1)
        self.ischanged = True

        return self.map_img
        
    def project_position(self, pos_x, pos_y, pos_yaw):
        """ 将世界坐标系的点记录到图像中，将改写原有图像
            当原有的图像发生过改变时，读入新的图像
        input:
          pos_x, pos_y, pos_yaw(deg)
        output:
          proj_img: 结果图像
        """
        if self.ischanged:
            proj_img = cv2.imread(self.map_path)
        else:
            proj_img = np.copy(self.map_img)

        car_img = self.car_logo.get_rot(pos_yaw)
        h,w,_ = car_img.shape
        pil_x = int(1.0 * pos_x * self.coef[2] + self.coef[0])
        pil_y = int(1.0 * pos_y * self.coef[3] + self.coef[1])
        sub_roi = proj_img[pil_y-h/2:pil_y+h/2, pil_x-w/2:pil_x+w/2,:]
        
        sub_roi[car_img!=0] = car_img[car_img!=0]
        return proj_img

    def disp_map(self):
        cv2.imshow("map",self.map_img)
        cv2.waitKey(0)

    def add_uncertainty(self, proj_img, uxy,minuxy,maxuxy, uab,minuab,maxuab):
        h,w = 50, 200
        bg = np.zeros((h,w,3),np.uint8)
        bg[5:15,5:15] = (0,220,30)
        bg[25:35,5:15] = (0,50,220)
        
        v1 = int((w-20) * (uxy - minuxy) /(maxuxy - minuxy)) 
        bg[5:15,20:20+v1] = (0,200,90)
    
        v2 = int((w-20) * (uab - minuab) /(maxuab - minuab)) 
        bg[25:35,20:20+v2] = (0,90,200)
        ph,pw,_ = proj_img.shape
        new_im = np.zeros((ph,pw+w,3), np.uint8)
        new_im[:,:pw,:] = proj_img[:]
        new_im[:h,pw:,:] = bg[:]
        
        return new_im
 
    def add_angle(self, proj_img, pos_a, pos_b):
        yaw = np.arccos(pos_a)
        yaw = np.rad2deg(yaw)
        yaw = np.int(yaw)
        if pos_b < 0:
            yaw = -yaw
        h,w = 102, 102
        bg = np.zeros((h,w,3),np.uint8)
        # 画坐标线
        bg[50:52,5:-5,:] = (0,200,90)
        bg[5:-5,50:52,:] = (0,200,90)
        m = 5
        cv2.line(bg, (w-5,50),(w-5-m,50-m), (0,200,90),1)
        cv2.line(bg, (w-5,51),(w-5-m,51+m), (0,200,90),1)
        cv2.line(bg, (50,5),(50+m,5+m), (0,200,90),1)
        cv2.line(bg, (51,5),(51-m,5+m), (0,200,90),1)
        
        p1 = (51,51)    # a, b
        s = 40
        p2 = (51 + int(s * pos_b),51 - int(s * pos_a))
        cv2.line(bg, p1,p2, (0,200,90),2)
        cv2.putText(bg,"yaw=%03d"%yaw,(10,100), cv2.FONT_HERSHEY_PLAIN, 1.0, (0,90,200), thickness = 1)
        
        ph,pw,_ = self.map_img.shape
        proj_img[ph-h:ph,pw:pw+w,:] = bg[:]
        return proj_img

if __name__=="__main__":
    pass

