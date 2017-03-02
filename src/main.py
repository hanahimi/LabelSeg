#-*-coding:UTF-8-*-
'''
Created on 2017��3��1��-����1:34:57
author: Gary-W
'''

import cv2
import numpy as np
import os
from config_parser import TextParser
parser = TextParser()
text_path = r"config.txt"
items_table = parser(text_path)

label_table = {}
cur_line_color = (0,0,200)
for key,item in items_table.items():
    if key.find("class_")==-1:
        continue
    try:
        id,color = item.split(' ')
        id = int(id)
        color = color[1:-1]
        color = tuple([int(c) for c in color.split(',')])
        label_table[id] = {"label":key, "color":color}
    except:
        pass
img_path = items_table["img_path"]
img_load = cv2.imread(img_path)
print("please input '1' to '9'")
h,w,_ = img_load.shape

pad = items_table["pad"]
linewidth = items_table["linewidth"]
img_draw = np.zeros((h+pad*2,w+pad*2,3),np.uint8)
img_label = np.zeros((h+pad*2,w+pad*2),np.uint8)
img_draw_stack = []
img_label_stack = []
_img_draw = np.zeros((h+pad*2,w+pad*2,3),np.uint8)
_img_label = np.zeros((h+pad*2,w+pad*2),np.uint8)
_img_draw[:] = img_draw[:]
_img_label[:] = img_label[:]
img_draw_stack.append(_img_draw)
img_label_stack.append(_img_label)

img_ploy = np.zeros((h+pad*2,w+pad*2,3),np.uint8)

mouse_act_down = False
cur_label = 0

# ��¼��ǰ����ε����е�
point_logs = []

def draw_foldline(img, pts):
    """ �������� """
    for i, _point in enumerate(pts):
        if i == 0:
            continue
        x0,y0 = point_logs[i-1]
        x1,y1 = point_logs[i]
        cv2.line(img, (x0,y0),(x1,y1),cur_line_color,linewidth)

def disp_gray(img2d):
    imgshow = img2d * 25
    return imgshow

def fill_ploygon(img, pts):
    img_ploy[:] = 0
    """ ���ƶ���� """
    pts0 = np.array(pts)
    pts0 = pts0.reshape((-1,1,2))
    cv2.polylines(img,[pts0],True,cur_line_color,linewidth)
    if cur_label in label_table:
        # ���ݴ�ͼ���ϻ���ɫ
        cv2.fillPoly(img_ploy, [pts0],cur_line_color)
        # �ð�͸���������ںϳɽ��
        img[img_ploy!=0] = np.uint8(img_ploy[img_ploy!=0]*0.3 + img[img_ploy!=0]*0.7)
        # �ڻҶ�ͼ���ϻ���ע���
        cv2.fillPoly(img_label, [pts0],cur_label)

def callback_draw_ploygon(event, x, y,flags,param):
    """ ����ն����
        x,y ��굱ǰλ��
    """
    global x0, y0
    
    # ���������ʱ���ص�ǰλ������
    if event == cv2.EVENT_LBUTTONDOWN:
        point_logs.append((x,y))
        # ��ͼ���л��ƹؼ���
        cv2.circle(img_draw,(x,y), 3, cur_line_color,-1)
        # ���ݵ�ǰlog��������
        draw_foldline(img_draw, point_logs)


# �ص�������OpenCV ���ڰ���һ��,
cv2.namedWindow('image')
# ���¼�
cv2.setMouseCallback('image',callback_draw_ploygon) 
while(1):
    img_roi = img_draw[pad:pad+w,pad:pad+h]
    img_roi[img_roi==0] = img_load[img_roi==0]
    cv2.imshow('image',img_draw)
    cv2.imshow('label',disp_gray(img_label))

    k=cv2.waitKey(1)&0xFF
    if 49 <= k <= 57:
        cur_label = k - 48
        cur_line_color = label_table[cur_label]['color']
        print("curlabel:",cur_label,label_table[cur_label]['label'])
    elif k == 48:
        cur_line_color = label_table[cur_label]['color']
        
        
    elif k==32:# ���ո� ���Ʊպ϶���� �������ɫ
        if len(point_logs) > 0:
            fill_ploygon(img_draw, point_logs)
            _img_draw = np.zeros((h+pad*2,w+pad*2,3),np.uint8)
            _img_label = np.zeros((h+pad*2,w+pad*2),np.uint8)
            _img_draw[:] = img_draw[:]
            _img_label[:] = img_label[:]
            img_draw_stack.append(_img_draw)
            img_label_stack.append(_img_label)
            point_logs = []
   
    elif k==ord('z'):# z ������һ�α�ע
        if len(img_draw_stack)>0 and len(img_label_stack)>0 :
            print("len(img_draw_stack)=", len(img_draw_stack))
            img_draw_stack.pop(-1)
            img_label_stack.pop(-1)
        if len(img_draw_stack)>0 and len(img_label_stack)>0 :
            img_draw[:] = img_draw_stack[-1]
            img_label[:] = img_label_stack[-1]
        
    elif k==13: # ��Enter�˳� �� ����
        img_sav = img_label[pad:pad+w,pad:pad+h]
        cv2.imwrite(img_path.split(".")[0]+"_seq.png",img_sav)
        print("save", img_path.split(".")[0] + "_seq.png")
        break
    
    elif k==27: # ��Esc�˳�
        print("esc")
        break

