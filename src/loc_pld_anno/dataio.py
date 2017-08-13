#-*-coding:UTF-8-*-
'''
Created on 2016年8月3日-上午11:15:25
author: Gary-W
数据的输入输出，读写保存操作
'''
import os
import pickle
import shutil

# 获取目录下，后缀为subfix的文件绝对路径列表，subfix为可变参数
def get_filelist(root_dir, *subfixs):
    """
    sample:
    get_filelist(r'../daytime_adaboost/pos',".png",".jpg")
    """
    p = []
    for subfix in subfixs:
        p.extend([os.path.join(root_dir,f) for f in os.listdir(root_dir) if f.endswith(subfix)])
    return p

# 获取目录下，后缀为subfix的文件名列表，subfix为可变参数
def get_filenamelist(root_dir, *subfixs):
    p = []
    for subfix in subfixs:
        p.extend([f for f in os.listdir(root_dir) if f.endswith(subfix)])
    return p



# 获取目录下，前缀为prefix的文件绝对路径列表，prefix为可变参数
def get_prefilelist(root_dir, *prefixs):
    p = []
    for prefixs in prefixs:
        p.extend([os.path.join(root_dir,f) for f in os.listdir(root_dir) if f.startswith(prefixs)])
    return p

# 获取目录及子目录下，后缀为subfix的文件绝对路径列表，subfix为可变参数
def get_walkfilelist(root_dir, *subfixs):
    fullpath = []       # 放置文件的系统绝对路径
    corr_path = []      # 放置文件在root_dir下的相对路径
    len_root = len(root_dir)
    for root, dirs, files in os.walk(root_dir): 
        for filespath in files:
            for subfix in subfixs:
                if filespath.endswith(subfix):
                    p = os.path.join(root,filespath)
                    fullpath.append(p)
                    corr_path.append(p[len_root+1:])    # 后退一个 "\"
    return fullpath, corr_path

# pickle 系列文件
def store_pickle(path, obj):
    try:
        with open(path, 'wb') as fw:
            pickle.dump(obj, fw)
    except IOError as ioerr:    print "IO Error:"+str(ioerr)+"in:\n"+path

def load_pickle(path):
    try:
        with open(path, 'rb') as fr:
            obj = pickle.load(fr)
            return obj
    except IOError as ioerr:    print "IO Error:"+str(ioerr)+"in:\n"+path

# 基于src_dir 和 dst_dir创建训练数据文件夹
def create_dirs(src_dir, dst_dir):
    """
    src_dir中包含了：
    class1，class2，...各文件夹
    dst_dir中包含：
    train, val, train.txt, val.txt
    """
    label_names = os.listdir(src_dir)
    for label in label_names:
        train_dir = os.path.join(dst_dir,"train", label)
        val_dir = os.path.join(dst_dir,"val", label)
        if not os.path.exists(train_dir):
            os.makedirs(train_dir)
        if not os.path.exists(val_dir):
            os.makedirs(val_dir)
    return label_names

# 将源目录系统复杂到目标目录系统中，包含相应后缀的文件
def copy_n_sel(src, dst, *ig_subfixs):
    if not os.path.exists(dst):
        os.makedirs(dst)
    _, sel_corr_paths = get_walkfilelist(src, ig_subfixs)
    dst_list = []
    for sel_p in sel_corr_paths:
        dst_path = os.path.join(dst, sel_p)
        src_path = os.path.join(src, sel_p)
        parent_dir = os.path.split(dst_path)[0]
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)
        print "copying ",dst_path
        shutil.copyfile(src_path,dst_path)
        dst_list.append(dst_path)
    return dst_list

# 查找根目录下具有目标文件/目录的盘符(只返回一个)
def getTargetDisk(tar_file="Location_PoseNet_Code_Dataset"):
    candidate = ["E:","F:","G:","H:","I:"]
    for d in candidate:
        if os.path.isdir(d):
            tmpath = os.path.join(d, tar_file)
            if os.path.exists(tmpath):
                return d
    print "no valid disk"
    # TODO: raise exception
    
if __name__=="__main__":
    pass
#     p_list = get_filelist(r'/home/hanahimi/project/BSD/daytime_adaboost/pos',".png",".jpg",".bmp")
#     print len(p_list)
    root_path = r"F:\2016-10-27"
    root_path2 = r"F:\2016-10-27_cpy"
#     copy_n_sel(root_path, root_path2, ".bmp")
    getTargetDisk()


