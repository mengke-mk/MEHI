################################
# Author   : septicmk
# Date     : 2015/07/25 10:44:53
# FileName : IO.py
################################

import skimage.external.tifffile as tiff
from MEHI.utils.tool import exeTime,bar
import numpy as np
import os

@exeTime
def load_tiff(pwd, start_index=None, end_index=None):
    '''
    Usage:
     - just read all the image under the pwd
    '''
    if os.path.isdir(pwd):
        img_stack = []
        names = []
        for imgname in os.listdir(pwd):
            if imgname.endswith('.tif'):
                names.append(imgname)
        names = sorted(names, key = lambda x: int(filter(str.isdigit, x)))
        if (start_index) and (end_index) and (0 <= start_index < end_index) and (start_index < end_index <= len(names)):
            names = names[start_index:end_index]
        for z,imgname in enumerate(names):
            msg = "reading %d-th frame" % (z+1)
            end = len(names)
            bar('info')(msg, z+1, end)
            img_pwd = os.path.join(pwd, imgname)
            if img_pwd.endswith('.tif'):
                img = tiff.imread(img_pwd)
                img_stack.append(img)
        return np.array(img_stack)
    else:
        return tiff.imread(pwd)

@exeTime 
def save_tiff(img_stack, pwd):
    '''
    Usage:
     - write the img_stack
    '''
    if pwd.endswith('.tif'):
        tiff.imsave(name, img_stack) 
    else:
        for z,frame in enumerate(img_stack):
            fname = pwd + '_%03d' % (z+1) + '.tif'
            dir, file = os.path.split(fname)
            if not os.path.exists(dir):
                os.makedirs(dir)
            tiff.imsave(fname, frame)

@exeTime
def load_table(pwd):
    import pandas as pd
    return pd.read_pickle(pwd)

@exeTime
def save_table(tab, pwd):
    import pandas as pd
    pd.to_pickle(pwd)
    pd.to_csv(pwd)
