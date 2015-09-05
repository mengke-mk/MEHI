################################
# Author   : septicmk
# Date     : 2015/09/05 16:58:05
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
        tiff.imsave(pwd, img_stack) 
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


@exeTime
def load_mha(fn):
    import zlib
    def _cast2int (l):
        l_new=[]
        for i in l:
            if i.is_integer(): l_new.append(int(i))
            else: l_new.append(i)
        return l_new
    
    _shiftdim = lambda x, n: x.transpose(np.roll(range(x.ndim), -n))

    if fn.endswith('.mha'):
        
        f = open(fn,'rb')
        objecttype='2dimg' ## On default the matrix is considered to be an image
        direction_cosines = None
        offset = None
        spacing = None
        size = None
        data_type = None
        data = None
        compressed = False
        ## Read mha header
        for r in range(20):
            row=f.readline()
            if row.startswith('TransformMatrix ='):
                row=row.split('=')[1].strip()
                direction_cosines=_cast2int(map(float, row.split()))
            elif row.startswith('Offset ='):
                row=row.split('=')[1].strip()
                offset=_cast2int(map(float, row.split()))
            elif row.startswith('ElementSpacing ='):
                row=row.split('=')[1].strip()
                spacing=_cast2int(map(float, row.split()))
            elif row.startswith('DimSize ='):
                row=row.split('=')[1].strip()
                size=map(int, row.split())
                if len(size) < 3:
                    objecttype = '2dimg'
                else:
                    objecttype = '3dimg'
            elif row.startswith('ElementNumberOfChannels = 3'):
                data='vf' ## The matrix is a vf
                size.append(3)
            elif row.startswith('ElementType ='):
                data_type=row.split('=')[1].strip()
            elif row.startswith('CompressedData = True'):
                compressed = True
            elif row.startswith('ElementDataFile ='):
                break
        
        ## Read raw data
        data=''.join(f.readlines())
        f.close()
        if compressed:
            data = zlib.decompress(data)
        
        ## Raw data from string to array
        if data_type == 'MET_SHORT':
            data=np.fromstring(data, dtype=np.int16)
            data_type = 'short'
        if data_type == 'MET_UINT':
            data=np.fromstring(data, dtype=np.uint32)
            data_type = 'int'
        elif data_type == 'MET_FLOAT':
            data=np.fromstring(data, dtype=np.float32)
            data_type = 'float'
        elif data_type == 'MET_DOUBLE':
            data=np.fromstring(data, dtype=np.float64)
            data_type = 'double'
        elif data_type == 'MET_UCHAR':
            data=np.fromstring(data, dtype=np.uint8)
            data_type = 'uchar'

        print size
        ## Reshape array
        if objecttype == '2dimg':
            data=data.reshape(size[1],size[0])
        elif objecttype == '3dimg':
            data=data.reshape(size[2],size[1],size[0])
        elif objecttype == 'vf':
            data=data.reshape(size[2],size[1],size[0],3)
            data=_shiftdim(data, 3).T

        return data
    elif not fn.endswith('.mha'): ## Extension file is not ".mha". It returns all null values
        raise NameError('The input file is not a mha file!')


