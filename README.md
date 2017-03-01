# LabelSeg
基于python和opencv的样本交互标注工具
（很简单，没有多余的GUI，只能用于全程手动的分割标注）
## Requirements
- python2.7
- python-opencv
- [option] eclipse

## Usage
在config.txt的img_path项处，填写目标待标注图片
运行main.py,显示两个窗口，分别为标注图像，和标注结果

类别设置参考config.txt

按键如下：
- 1 to 9键 切换类别
- 单击鼠标左键：在标注窗口滑动
- 空格：闭合多边形，并更新标注结果
- z键：撤销最近的一次“完整的”标注操作
- Esc：退出标注并自动保存标注结果，保存路径为输入图像的同一文件夹下，并添加seg后缀

## Trick
先标注层级较低的物体，使用非常粗略的标注（画到别的物体上），再标注细节，用较上层的物体覆盖
