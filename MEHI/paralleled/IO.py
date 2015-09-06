import skimage.external.tifffile as tiff
import numpy as np
import os
from MEHI.utils.tool import exeTime

@exeTime
def load_tiff(sc, pwd, start_index=None, end_index=None):
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
        n = len(names)
        def func(name):
            img_pwd = os.path.join(pwd, name)
            if img_pwd.endswith('.tif'):
                img = tiff.imread(img_pwd)
            return img
        rdd_file = sc.parallelize(names)
        return np.squeeze(np.array(rdd_file.map(func).collect()))
    else:
        return tiff.imread(pwd)

@exeTime
def save_tiff(img_stack, pwd):
    '''
    Usage:
     - write the img_stack
    '''
    if pwd.endswith('.tif'):
        tiff.imsave(pwd, img_stack) 
    else:
        for z, frame in enumerate(img_stack):
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
