################################
# Author   : septicmk
# Date     : 2015/09/05 16:55:15
# FileName : preprocess.py
################################

import skimage.external.tifffile as tiff
import numpy as np
import math
from MEHI.utils.tool import exeTime

def stripe_removal(rdd):
    '''
    Usage:
     - remove the stripe
     - (discarded)
    '''
    import skimage.morphology as mor
    def func(frame):
        _dtype = frame.dtype
        kernel = mor.disk(3)
        frameWP = frame - mor.white_tophat(frame, kernel) * (mor.white_tophat(frame, kernel) > 1000).astype(float)
        kernel = mor.rectangle(25, 1)
        closed = mor.closing(frameWP, kernel)
        opened = mor.opening(closed, kernel)
        result = ((frameWP.astype(float) / opened.astype(float)) * 3000.0)
        return result.astype(_dtype)
    return rdd.map(func)

def intensity_normalization(rdd, dtype=None):
    from MEHI.udf._intensity import normalization
    def func(frame):
        return normalization(frame, dtype)
    return rdd.map(func)

def saturation(rdd, precent):
    from MEHI.udf._intensity import saturation
    def func(frame):
        return saturation(frame, precent)
    return rdd.map(func)
        

def flip(rdd):
    def func(frame):
        return frame[:,::-1]
    return rdd.map(func)
    
def invert(rdd):
    def func(frame):
        if frame.dtype == np.uint8:
            return np.array(map(lambda p: 255-p, frame))
        elif frame.dtype == np.uint16:
            return np.array(map(lambda p: 65535-p, frame))
        else :
            return np.array(map(lambda p: p, frame))
    return rdd.map(func)

def black_tophat(rdd, size=15):
    '''
    Usage:
     - black tophat 
     - change the circle to pie
    Args:
     - size: the smooth size 
    '''
    import skimage.morphology as mor
    def func(frame):
        return mor.black_tophat(frame, mor.disk(size))
    return rdd.map(func)

def subtract_Background(rdd, size=12):
    '''
    Usage:
     - subtrackt Background (based on C)
    args:
     - radius: the smooth size
    '''
    from MEHI.udf._subtract_bg import subtract_Background
    def func(frame):
        return subtract_Background(frame, size)
    return rdd.map(func)

def shrink(rdd, shrink_size=2):
    def func(frame):
        _X,_Y = frame.shape
        _sX, _sY = _X / shrink_size, _Y / shrink_size
        shrink_frame = np.zeros([_sX,_sY])
        for i in range(_sX):
            for j in range(_sY):
                shrink_frame[i][j] = sum(frame[i*shrink_size:(i+1)*shrink_size,j*shrink_size:(j+1)*shrink_size].flatten()) / (shrink_size*shrink_size)
        return shrink_frame.astype(frame.dtype)
    return rdd.map(func)

@exeTime
def projection(img_stack, method='max'):
    if method == 'max':
        proj = img_stack.max(axis=0)
    elif method == 'min':
        proj = img_stack.min(axis=0)
    elif method == 'mean':
        proj = img_stack.mean(axis=0)
    else:
        raise "Bad Projection Method", method
    return proj

def smooth(rdd, smooth_size):
    from skimage.morphology import disk
    from skimage.filters import rank
    def func(frame):
        smoothed = rank.median(frame,disk(smooth_size))
        smoothed = rank.enhance_contrast(smoothed, disk(smooth_size))
        return smoothed
    return rdd.map(func)

@exeTime
def blockshaped_all(img_stack, nrows, ncols):
    def blockshaped(arr, nrows, ncols):
        h, w = arr.shape
        return (arr.reshape(h//nrows, nrows, -1, ncols)
                   .swapaxes(1,2)
                   .reshape(-1, nrows, ncols))
    arr_list = []
    for x in img_stack:
        for frame in blockshaped(x, nrows, ncols):
            arr_list.append(frame)
    return np.array(arr_list)

@exeTime
def recovershape_all(img_stack, nrows, ncols):
    def recovershape(arr_list, nrows, ncols):
        y = []
        for i in range(nrows):
            x = []
            for j in range(ncols):
                x.append(arr_list[i*ncols + j])
            y.append(np.hstack(tuple(x)))
        return np.vstack(tuple(y))
    step = nrows*ncols
    ori = []
    for i in range(0,img_stack.shape[0],step):
        arr = img_stack[i:i+step]
        ori.append(recovershape(arr, nrows, ncols))
    return np.array(ori)
       
if __name__ == '__main__':
    print 'OK'
    pass

