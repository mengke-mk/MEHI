################################
# Author   : septicmk
# Date     : 2015/08/19 15:51:16
# FileName : mha2tiff.py
################################

import skimage.external.tifffile as tiff
import MEHI.utils.mha as mha
import numpy as np
import os
import MEHI.serial.preprocess as prep


input_pwd = '/mnt/xfs_snode21/0401mha/acme_test.tif'
output_pwd = '/mnt/xfs_snode21/0401mha/'

def save_tiff(img_stack, pwd):
    if pwd.endswith('.tif'):
        tiff.imsave(pwd, img_stack) 
    else:
        for z,frame in enumerate(img_stack):
            fname = pwd + '_%03d' % (z+1) + '.tif'
            dir, file = os.path.split(fname)
            if not os.path.exists(dir):
                os.makedirs(dir)
            tiff.imsave(fname, frame)

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
            img_pwd = os.path.join(pwd, imgname)
            if img_pwd.endswith('.tif'):
                img = tiff.imread(img_pwd)
                img_stack.append(img)
        return np.array(img_stack)
    else:
        return tiff.imread(pwd)

def cover(conf='mha2tiff'):
    if conf == 'm':
        for lists in os.listdir(input_pwd):
            path = os.path.join(input_pwd, lists)
            if path.endswith('.mha'):
                x = mha.read_mha(path)
                path = os.path.basename(path)
                path = os.path.join(output_pwd, path)
                name = os.path.splitext(path)[0] + '.tif'
                print name
                save_tiff(x, name)
    elif conf == 'tiff2mha':
        for lists in os.listdir(input_pwd):
            path = os.path.join(input_pwd, lists)
            if path.endswith('.tif'):
                x = load_tiff(path)
                path = os.path.basename(path)
                path = os.path.join(output_pwd, path)
                name = os.path.splitext(path)[0] + '.mha'
                print name
                mha.write_mha(x, name)


if __name__ == '__main__':
    #cover(conf='tiff2mha')
    x = load_tiff(input_pwd)
    x = prep.intensity_normalization(x,8)
    mha.write_mha(x, output_pwd+'acme_test.mha')



