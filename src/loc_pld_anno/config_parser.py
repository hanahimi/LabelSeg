#-*-coding:UTF-8-*-
'''
Created on 2017��1��12��-����9:42:58
author: Gary-W
'''
class TextParser:
    def __init__(self):
        self.text_data = []
        self.items_table = {}
    
    def __call__(self, text_path):
        """ ��һ�������ļ�����Ϊ��Ŀ�ֵ�
            * �����������Ϊһ����������
        input:
          text_path��Ŀ�������ı���·��
        output:
          items_table���������ֵ�
        """
        self.fetch_setting_text(text_path, "#")
        self.build_table(self.text_data)
        return self.items_table
        
    def remove_space(self, src_str):
        """ ���ַ���ȥ�����пհ׷�
        input:
          src_str��ԭʼ�ַ���
        output:
          dst_str: ���˺��str
        """
        dst_str = src_str.strip("\t") # ɾ������tab
        dst_str = dst_str.rstrip(" ").lstrip(" ") # ɾ����������space
        return dst_str
        
    def fetch_setting_text(self, text_path, headmask="#"):
        """ ��ȡ�����ļ�,�����˵�������
        �����а������������η����У����У�tab�У�ȫ�ո���
        ע�⣺��Ч�ı��в��ܴ����������" ","\t",etc�����ᱻ�޸�
        input:
          text_path��Ŀ�������ı���·��
          headmask: ���˱�־������headmask֮����ı��ᱻȥ��
        """
        self.text_data = []
        with open(text_path) as f:
            for line in f.readlines():
                line = line.strip("\n") # ɾ������\n
                # ɾ������ headmask ֮��Ĳ���
                mask_id = line.find(headmask)
                if mask_id != -1:
                    line = line[:mask_id]
                line = self.remove_space(line)
                if line == "":          # ȥ������
                    continue
                self.text_data.append(line)
        if not self.text_data:
            print "none text has been loaded"
    
    def __trans_items(self, s):
        """ ����s��״̬���Զ�ת��Ϊ��Ӧ������
        input:
          s�������ַ���
        return:
          s_data���Զ�������
        """
        s_data = self.remove_space(s)   # ���ڱ��������л��пհ׷�
        
        if "'" in s or '"' in s:
            s_data = s_data.rstrip("'").lstrip("'")
            s_data = s_data.rstrip('"').lstrip('"')
        
        elif "." in s_data or (s_data[-1]=='f'):
            s_data = float(s_data)
        
        elif s_data.isdigit() or \
            ((s_data[0]=="-" or s_data[0]=="+") and s_data[1:].isdigit()):
            s_data = int(s_data)

        elif s_data[-1]=="%":
            s_data = float(s_data)/100

        elif s_data.find("e") != -1:
            eid = s_data.find("e")
            a = float(s_data[:eid])
            b = int(s_data[eid+1:])
            s_data = a * (10**b)
            
        else:
            try:
                s_data = int(s_data)
            except:
                s_data = None
        
        return s_data
             
    def build_table(self, text_list):
        """ ���ı���𣨾������ˣ�����Ϊ�������ֵ�
        �ֵ��е�Ԫ�ػ�����ı���ʽ��ת��Ϊ��ͬ���͵�ֵ, ������
        �ַ�����"*"
        ���飺[*],�������ͻ������,����Ϊ������[],�������[*,],��Ԫ������[,]
        ������eg. 123
        ������: eg. 123.0
        Ŀǰ���ı��б������":"�ָ�������ܱ������ɼ�ֵ��;
        ͬʱ�������������ظ�, ������������Ŀո�
        input:
          text_list����Ч�ı����б�
        return:
          self.items_table���������ֵ�
        """
        self.items_table = {}
        for _id, line in enumerate(text_list):
            # ��ʹ��split�Ǳ���value���� ":", ��Ϊ�����׸�":"
            spid = line.find(":")
            if spid == -1: continue
            items = (line[:spid], line[spid+1:])
            key = self.remove_space(items[0])
            value = self.remove_space(items[1])
            if key not in self.items_table:
                self.items_table[key] = None
            # ���ж��Ƿ�Ϊ����(�����飬Ԫ��Ϊ�յ����ݣ���Ч����)
            if ("[","]") == (value[0],value[-1]):
                value = value[1:-1]
                self.items_table[key] = []
                value = self.remove_space(value)
                if value == "": continue 
                value = value.split(",")
                for v in value:
                    self.items_table[key].append(self.__trans_items(v))
            else:
                self.items_table[key] = self.__trans_items(value)
        
if __name__=="__main__":
    pass
    parser = TextParser()
    text_path = r"runtime_setting.txt"
    items_table = parser(text_path)
    print items_table
    
