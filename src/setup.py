#-*-coding:UTF-8-*-
'''
Created on 2016年6月20日-下午2:38:09
author: Gary-W
'''
# 当代码编辑好之后，在cmd中：python setup.py py2exe，生成exe文件
from distutils.core import setup
import py2exe

setup(console=['main.py'])

if __name__=="__main__":
    pass

