step1： 

将bev的路径替换到 runtime_setting.txt 的 bev_root 项中，两边有""
运行pose_maker.py

鼠标左键单击： 添加一个新的位姿
鼠标左键长按： 位姿逆时针旋转
鼠标右键长按： 位姿顺时针旋转

键盘
z： 删除最近记录并将操作目标切换到上一个标记
c:	清除所有标记，并将标记id设置为0
q：后退一个单位帧（10帧一个BEV）
e：前进一个单位帧（10帧一个BEV）


当地图上有标注的记录时
1：逆时针微调角度
2：顺时针微调角度
wasd ： 单个像素微调位置


step 2:
执行pose_insert.py
显示 全局路线
按任意键
显示动画
按任意键 退出

得到 新的pos.txt

step 3:
将 pos.txt 和 bev文件夹放在一起给我

note:
如果 文件夹中有pose_marker.txt 则恢复现场、
所以新建标注时，要把该文件呢删掉