#-*-coding:UTF-8-*-
'''
Created on 2017��1��12��-����3:30:08
author: Gary-W

��ͼ���ƣ������ͶӰ
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
    """ ��ͼ������
    ���ڽ���������ӳ�䵽ͼƬ�ϣ�����ʹ�������ļ����в�������
    attribute:
      map_img: ԭʼ��ͼ����
      coef: ����ͶӰ����
    """
    def __init__(self):
        self.map_path = r"map.jpg"
        self.map_img = cv2.imread(self.map_path)
        self.h = self.map_img.shape[0]
        self.w = self.map_img.shape[1]
        
        self.coef = [42,413, 7, -7]
        self.car_logo = CarModel()
        self.result = np.copy(self.map_img)
        
    def project_position(self, pos_x, pos_y, pos_yaw):
        """ ����������ϵ�ĵ��¼��ͼ���У�����С��
            ��ԭ�е�ͼ�������ı�ʱ�������µ�ͼ��
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


if __name__=="__main__":
    pass
    pm = PosMap()
    pm.project_position(0,0,0)
    cv2.imshow("ss", pm.result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    