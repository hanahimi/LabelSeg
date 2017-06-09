#-*-coding:UTF-8-*-
'''
Created on 2017年5月25日-下午5:19:58
author: Gary-W

标记输入指令解析器
'''


class CommandParser:
    def __init__(self):
        pass
    
    def trans(self,s_cmd):
        items = s_cmd.strip("\n").split(' ')
        if items[0] == 'add':
            # 添加新的关键帧
            if len(items)==2:
                frame_id = int(items[1])
                return frame_id




if __name__=="__main__":
    pass

