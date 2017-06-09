#-*-coding:UTF-8-*-
'''
Created on 2017年5月25日-下午3:17:59
author: Gary-W
'''
import numpy as np

class VPose:
    """
    车辆在图像坐标系上的位置
    """
    def __init__(self,id, x=100,y=100,deg=0.):
        self.id = id    # 帧号
        self.x = x
        self.y = y
        self.deg = deg

    def rotate_clk_wise(self,d_deg,ori=1):
        self.deg += ori * d_deg
        rad = np.deg2rad(self.deg)
        a = np.cos(rad)
        b = np.sin(rad)
        rad = np.arccos(a)
        if b < 0:
            rad *= -1
        self.deg = np.rad2deg(rad)
        

def save_vpose_arr(filename, vpose_arr):
    """
    按照帧号顺序从小到大排列标记，并保存在txt中
    """
    # sort
    def comp(vpa, vpb):
        if vpa.id < vpb.id:
            return -1
        elif vpa.id > vpb.id:
            return 1
        else:
            return 0
    vpose_arr.sort(comp)

    # save
    with open(filename,"w") as f:
        for vp in vpose_arr:
            s = "%05d %d %d %f\n" % (vp.id, vp.x, vp.y, vp.deg)
            f.write(s)
    print("save file in %s" % filename)
    
if __name__=="__main__":
    pass
    vp1 = VPose(1,2,3,4)
    vp2 = VPose(5,6,7,8)
    vpose_arr = [vp1, vp2]
    filename = "pose.txt"
    save_vpose_arr(filename, vpose_arr)



