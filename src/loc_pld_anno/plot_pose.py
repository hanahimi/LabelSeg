#-*-coding:UTF-8-*-
'''
Created on 2017年6月12日-上午10:45:05
author: Gary-W
'''
import os
from config_parser import TextParser
from vehicle_model import CanMatchLog,VehicleMotion, can_insert
from draw_map import PosMap
import numpy as np

can_filename = r"E:\LOC_Code_Dataset\saic_dataset\oflim相机数据\ofilm_raw_data_ug\20170807_EP21_car02\01_入口进车库分别在左中右车道绕外圈多次\can_match.txt"
can_dir = os.path.split(can_filename)[0]
img_filename = can_dir + r"\pose_map.jpg"
note_filename = can_dir + r"\pose_setting.cfg"
start = 1001
stop = 1500
start_point = [0, 0, 0] # xm, ym, deg
rot_table = {}
key_point = [1058,1081,1105,1124,1234]


def save_fit_table(note_filename):
    with open(note_filename,"w") as f:
        line = "start_point = "+str(start_point)+" # xm, ym, deg\n"
        f.write(line)
        line = "rot_table = "+str(rot_table)+"\n"
        f.write(line)
        line = "key_point = "+str(key_point)+"\n"
        f.write(line)
        
    
def read_can_log(can_filename):
    can_match_logs = {}
    with open(can_filename) as f:
        lines = f.readlines()
        for line in lines: 
            _can_log = CanMatchLog(line)
            can_match_logs[_can_log.data["frameID"]] = _can_log
    return can_match_logs

def generate_pose(can_match_logs):
    cfg_parser = TextParser()
    cfg_tabel = cfg_parser("data/vehicle_config.cfg")
    vm = VehicleMotion(cfg_tabel["wheel_base"],cfg_tabel["vehicle_width"])
    pose = []
    vm.setPosition(start_point[0],start_point[1],start_point[2])
    _vhcl_can_data = None
    for _i,vhcl_can_data in enumerate(can_match_logs):
        if _i > 0:
            print _i,
            times = (vhcl_can_data.data["time_stamp"] - _vhcl_can_data.data["time_stamp"]) #/ time_unit
            vm.traject_predict_world(vhcl_can_data, times)
            if vhcl_can_data.data["frameID"] in rot_table:
                vm.theta += np.deg2rad(rot_table[vhcl_can_data.data["frameID"]])
            pose.append((vm.pos.x, vm.pos.y, vm.theta, vm.radius, int(vhcl_can_data.data["frameID"])))
#             print vhcl_can_data.strframeId, vm.pos.x, vm.pos.y
        _vhcl_can_data =  vhcl_can_data
    return pose

def disp_pose(vm_pose):
    cfg_parser = TextParser()
    cfg_tabel = cfg_parser("data/vehicle_config.cfg")
    mapper = PosMap(cfg_tabel)
    for pos in vm_pose:
        pos_x, pos_y, pos_yaw, r, id_ = pos
        if id_ >= start:
            mapper.mark_position(pos_x, pos_y, pos_yaw, False)
        if id_ == stop:
            break
    for pos in vm_pose:
        pos_x, pos_y, pos_yaw, r, id_ = pos
        if id_ >= start:
            if id_ in key_point:
                print id_
                mapper.mark_position(pos_x, pos_y, pos_yaw, True)
                mapper.mark_pose_id(pos_x, pos_y, pos_yaw, id_)
        if id_ == stop:
            break
    mapper.disp_map(img_filename)

def save_pose(pos_filename, vm_pose):
    cfg_parser = TextParser()
#     cfg_tabel = cfg_parser("data/vehicle_config.cfg")
    with open(pos_filename, "w") as f:
        for i, pose in enumerate(vm_pose):
            a = np.cos(pose[2])
            b = np.sin(pose[2])
            t = np.arccos(a) if b > 0 else -np.arccos(a)
            msg = "%05d %f %f %f\n" % ( pose[4], pose[0],pose[1],t)
            f.write(msg)

def main():
#     can_filename = r"E:\saic_ug\2\can_match.txt"
    can_match_logs = read_can_log (can_filename)
    vm_pose = generate_pose(can_match_logs)
    disp_pose(vm_pose)
    pos_filename = can_filename[:-4]+"_pos.txt"
    save_pose(pos_filename, vm_pose)
    save_fit_table(note_filename)
    

if __name__=="__main__":
    pass
    main()






