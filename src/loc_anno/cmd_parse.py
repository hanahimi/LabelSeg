#-*-coding:UTF-8-*-
'''
Created on 2017��5��25��-����5:19:58
author: Gary-W

�������ָ�������
'''


class CommandParser:
    def __init__(self):
        pass
    
    def trans(self,s_cmd):
        items = s_cmd.strip("\n").split(' ')
        if items[0] == 'add':
            # ����µĹؼ�֡
            if len(items)==2:
                frame_id = int(items[1])
                return frame_id




if __name__=="__main__":
    pass

