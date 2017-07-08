#-*-coding:UTF-8-*-
'''
Created on 2017年1月12日-上午9:42:58
author: Gary-W
'''
class TextParser:
    def __init__(self):
        self.text_data = []
        self.items_table = {}
    
    def __call__(self, text_path):
        """ 将一个配置文件解析为项目字典
            * 将该类对象作为一个函数调用
        input:
          text_path：目标配置文本的路径
        output:
          items_table：配置项字典
        """
        self.fetch_setting_text(text_path, "#")
        self.build_table(self.text_data)
        return self.items_table
        
    def remove_space(self, src_str):
        """ 对字符串去掉所有空白符
        input:
          src_str：原始字符串
        output:
          dst_str: 过滤后的str
        """
        dst_str = src_str.strip("\t") # 删除所有tab
        dst_str = dst_str.rstrip(" ").lstrip(" ") # 删除两侧所有space
        return dst_str
        
    def fetch_setting_text(self, text_path, headmask="#"):
        """ 读取配置文件,并过滤掉特殊行
        特殊行包括：带有屏蔽符的行，空行，tab行，全空格行
        注意：有效文本中不能带有特殊符（" ","\t",etc），会被修改
        input:
          text_path：目标配置文本的路径
          headmask: 过滤标志符，带headmask之后的文本会被去除
        """
        self.text_data = []
        with open(text_path) as f:
            for line in f.readlines():
                line = line.strip("\n") # 删除所有\n
                # 删除包括 headmask 之后的部分
                mask_id = line.find(headmask)
                if mask_id != -1:
                    line = line[:mask_id]
                line = self.remove_space(line)
                if line == "":          # 去除空行
                    continue
                self.text_data.append(line)
        if not self.text_data:
            print "none text has been loaded"
    
    def __trans_items(self, s):
        """ 根据s的状态，自动转换为对应的类型
        input:
          s：不明字符串
        return:
          s_data：自动类型项
        """
        s_data = self.remove_space(s)   # 用于避免数组中还有空白符
        
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
        """ 将文本类别（经过过滤）解析为配置项字典
        字典中的元素会根据文本格式被转换为不同类型的值, 包括：
        字符串："*"
        数组：[*],混合数组,可以为空数组[],包含空元素数组[*,],空元素数组[,],  数组元素不能为数组
        整数：eg. 123
        浮点数: eg. 123.0
        目前，文本中必须包含":"分割符，才能被解析成键值对;
        同时键名不可以有重复, 不可以有两侧的空格
        input:
          text_list：有效文本的列表
        return:
          self.items_table：配置项字典
        """
        self.items_table = {}
        for _id, line in enumerate(text_list):
            # 不使用split是避免value出现 ":", 改为查找首个":"
            spid = line.find(":")
            if spid == -1: continue
            items = (line[:spid], line[spid+1:])
            key = self.remove_space(items[0])
            value = self.remove_space(items[1])
            if key not in self.items_table:
                self.items_table[key] = None
            # 先判断是否为数组(空数组，元素为空的数据，无效数组)
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
    
