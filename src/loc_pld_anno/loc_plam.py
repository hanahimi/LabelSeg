#-*-coding:UTF-8-*-
'''
Created on 2017年8月11日-上午11:34:18
author: Gary-W
'''
import cv2

class PkPlam:
    def __init__(self, x_offset=0, y_offset=0):
        self.bg = cv2.imread("plam.jpg")
        self.h = self.bg.shape[0]
        self.w = self.bg.shape[1]
        
        self.key_log = []
        self.x_offset = x_offset
        self.y_offset = y_offset
    
    def updateDisplayer(self):
        if len(self.key_log) > 0:
            ss = "".join(self.key_log)
            cv2.putText(self.bg, ss, (67,62), cv2.FONT_HERSHEY_PLAIN, 2.0,(200,200,200),thickness=2)
        
    def clear(self):
        self.key_log = []
        self.bg[32:69,56:245,:] = 0
    
    def getKey(self,x,y):
        x -= self.x_offset
        y -= self.y_offset
        d = 2
        if (18-d < x < 65+d) and (100-d < y < 140+d):
            return "A"
        elif (18-d < x < 65+d) and (159-d < y < 200+d):
            return "C"
        elif (18-d < x < 65+d) and (217-d < y < 261+d):
            return "E"
        elif (82-d < x < 131+d) and (100-d < y < 140+d):
            return "B"
        elif (82-d < x < 131+d) and (159-d < y < 200+d):
            return "D"
        elif (82-d < x < 131+d) and (217-d < y < 261+d):
            return "F"

        elif (22-d < x < 66+d) and (279-d < y < 324+d):
            return "+"
        elif (82-d < x < 131+d) and (279-d < y < 324+d):
            return "-"

        elif (151-d < x < 197+d) and (99-d < y < 138+d):
            return "1"
        elif (216-d < x < 260+d) and (99-d < y < 138+d):
            return "2"
        elif (281-d < x < 324+d) and (99-d < y < 138+d):
            return "3"
        elif (151-d < x < 197+d) and (158-d < y < 197+d):
            return "4"
        elif (216-d < x < 260+d) and (158-d < y < 197+d):
            return "5"
        elif (281-d < x < 324+d) and (158-d < y < 197+d):
            return "6"
        elif (151-d < x < 197+d) and (220-d < y < 260+d):
            return "7"
        elif (216-d < x < 260+d) and (220-d < y < 260+d):
            return "8"
        elif (281-d < x < 324+d) and (220-d < y < 260+d):
            return "9"
        elif (151-d < x < 197+d) and (280-d < y < 322+d):
            return "0"
        elif (216-d < x < 326+d) and (280-d < y < 322+d):
            return "Enter"

        elif (265-d < x < 296+d) and (31-d < y < 71+d):
            return "Clear"

        return 0
    

if __name__=="__main__":
    pass
    pp = PkPlam()
    x = 112
    y = 211
    key =  pp.getKey(x, y)
    if key != 0:
        pp.key_log.append(key)
    
    x = 172
    y = 103
    key =  pp.getKey(x, y)
    if key != 0:
        pp.key_log.append(key)
    
    x = 307
    y = 172
    key =  pp.getKey(x, y)
    if key != 0:
        pp.key_log.append(key)
    
    
    pp.updateDisplayer()
    cv2.imshow("final",pp.bg)
    cv2.waitKey(0)
    
    
    
    