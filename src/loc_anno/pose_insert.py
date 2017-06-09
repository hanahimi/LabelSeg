#-*-coding:UTF-8-*-
'''
Created on 2017年5月25日-下午8:01:45
author: Gary-W

基于pose_remark 文件的关键帧进行插值
'''
from vpose import VPose 
import config_parser as cfg_parser
from render import anime_check_pose,recover_index
import numpy as np

mark_file = "pose_mark.txt"

vpose_arr = []
with open(mark_file) as mf:
    lines = mf.readlines()
    for line in lines:
        fid,x,y,deg = line.strip("\n").split(" ")
        vp = VPose(int(fid), int(x), int(y), float(deg))
        vpose_arr.append(vp)
        
n_mark = len(vpose_arr)

id_all = []
x_all = []
y_all = []
deg_all = []
vp_all = []
for i in range(1,n_mark):
    id_op = vpose_arr[i-1].id
    id_ed = vpose_arr[i].id
    xd = 1.0*(vpose_arr[i].x - vpose_arr[i-1].x) / (id_ed - id_op)
    yd = 1.0*(vpose_arr[i].y - vpose_arr[i-1].y) / (id_ed - id_op)
   
    ai = np.cos(np.deg2rad(vpose_arr[i].deg))
    bi = np.sin(np.deg2rad(vpose_arr[i].deg))
    ai_ = np.cos(np.deg2rad(vpose_arr[i-1].deg))
    bi_ = np.sin(np.deg2rad(vpose_arr[i-1].deg))
    ad = 1.0*(ai - ai_) / (id_ed - id_op)
    bd = 1.0*(bi - bi_) / (id_ed - id_op)
     
    for j in range(id_ed - id_op):
        idj = id_op + j
        xj = vpose_arr[i-1].x + j * xd
        yj = vpose_arr[i-1].y + j * yd
        
        aj = np.cos(np.deg2rad(vpose_arr[i-1].deg)) + j*ad
        bj = np.sin(np.deg2rad(vpose_arr[i-1].deg)) + j*bd
        nj = np.sqrt(aj**2 + bj**2)
        aj /= nj
        bj /= nj
        degj = np.rad2deg(np.arccos(aj))
        if bj<0:
            degj *= -1
        vp = VPose(idj, xj, yj, degj)
        vp_all.append(vp)
vp_all.append(vpose_arr[-1])    # 补充最后的关键帧

# 保存最终pos文件
config_path = r"runtime_setting.txt"
cfgpar = cfg_parser.TextParser()
cfg = cfgpar(config_path)
pft = cfg["project_factors"]
pose_offset = cfg["world_center_offset"]

filename = "pos.txt"
with open(filename,"w") as f:
    for vp in vp_all:
        wx = 1.0*(vp.x - pft[0])/pft[2] - pose_offset[0]
        wy = 1.0*(vp.y - pft[1])/pft[3] - pose_offset[1]
        vp.rotate_clk_wise(0, 1)
        s = "%05d,%f %f %f\n" % (vp.id, wx, wy, np.deg2rad(vp.deg))
        f.write(s)
    print("save file in %s" % filename)

# 检查pos文件
config_path = r"runtime_setting.txt"
cfgpar = cfg_parser.TextParser()
cfg_table = cfgpar(config_path)

log_path = r"pos.txt"
recover_index(log_path, cfg_table)
anime_check_pose(log_path, cfg_table)

if __name__=="__main__":
    pass

