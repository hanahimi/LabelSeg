#-*-coding:UTF-8-*-
'''
Created on 2016��8��3��-����11:15:25
author: Gary-W
���ݵ������������д�������
'''
import os
import pickle
import shutil

# ��ȡĿ¼�£���׺Ϊsubfix���ļ�����·���б�subfixΪ�ɱ����
def get_filelist(root_dir, *subfixs):
    """
    sample:
    get_filelist(r'../daytime_adaboost/pos',".png",".jpg")
    """
    p = []
    for subfix in subfixs:
        p.extend([os.path.join(root_dir,f) for f in os.listdir(root_dir) if f.endswith(subfix)])
    return p

# ��ȡĿ¼�£���׺Ϊsubfix���ļ����б�subfixΪ�ɱ����
def get_filenamelist(root_dir, *subfixs):
    p = []
    for subfix in subfixs:
        p.extend([f for f in os.listdir(root_dir) if f.endswith(subfix)])
    return p



# ��ȡĿ¼�£�ǰ׺Ϊprefix���ļ�����·���б�prefixΪ�ɱ����
def get_prefilelist(root_dir, *prefixs):
    p = []
    for prefixs in prefixs:
        p.extend([os.path.join(root_dir,f) for f in os.listdir(root_dir) if f.startswith(prefixs)])
    return p

# ��ȡĿ¼����Ŀ¼�£���׺Ϊsubfix���ļ�����·���б�subfixΪ�ɱ����
def get_walkfilelist(root_dir, *subfixs):
    fullpath = []       # �����ļ���ϵͳ����·��
    corr_path = []      # �����ļ���root_dir�µ����·��
    len_root = len(root_dir)
    for root, dirs, files in os.walk(root_dir): 
        for filespath in files:
            for subfix in subfixs:
                if filespath.endswith(subfix):
                    p = os.path.join(root,filespath)
                    fullpath.append(p)
                    corr_path.append(p[len_root+1:])    # ����һ�� "\"
    return fullpath, corr_path

# pickle ϵ���ļ�
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

# ����src_dir �� dst_dir����ѵ�������ļ���
def create_dirs(src_dir, dst_dir):
    """
    src_dir�а����ˣ�
    class1��class2��...���ļ���
    dst_dir�а�����
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

# ��ԴĿ¼ϵͳ���ӵ�Ŀ��Ŀ¼ϵͳ�У�������Ӧ��׺���ļ�
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

# ���Ҹ�Ŀ¼�¾���Ŀ���ļ�/Ŀ¼���̷�(ֻ����һ��)
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


