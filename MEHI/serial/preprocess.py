################################
# Author   : septicmk
# Date     : 2015/09/05 16:55:37
# FileName : preprocess.py
################################

import skimage.external.tifffile as tiff
import numpy as np
import math
from MEHI.utils.tool import exeTime

@exeTime
def stripe_removal(img_stack):
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
    return np.array(map(func, img_stack)).astype(img_stack[0].dtype)

@exeTime
def intensity_normalization(img_stack, dtype=None):
    from MEHI.udf._intensity import normalization
    def func(frame):
        return normalization(frame, dtype)
    return np.array(map(func, img_stack))

@exeTime
def saturation(img_stack, precent):
    from MEHI.udf._intensity import saturation
    def func(frame):
        return saturation(frame, precent)
    return np.array(map(func, img_stack))

@exeTime
def flip(img_stack):
    def func(frame):
        return frame[:,::-1]
    return np.array(map(func, img_stack))
    
@exeTime
def invert(img_stack):
    def func(frame):
        if frame.dtype == np.uint8:
            return np.array(map(lambda p: 255-p, frame))
        elif frame.dtype == np.uint16:
            return np.array(map(lambda p: 65535-p, frame))
        else :
            return np.array(map(lambda p: p, frame))
    return np.array(map(func, img_stack))


@exeTime
def black_tophat(img_stack, size=15):
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
    return np.array(map(func, img_stack))

@exeTime
def subtract_Background(img_stack, size=12):
    '''
    Usage:
     - subtrackt Background (based on C)
    args:
     - radius: the smooth size
    '''
    from MEHI.udf._subtract_bg import subtract_Background
    def func(frame):
        return subtract_Background(frame, size)
    return np.array(map(func, img_stack))

@exeTime
def shrink(img_stack, shrink_size=2):
    def func(frame):
        _X,_Y = frame.shape
        _sX, _sY = _X / shrink_size, _Y / shrink_size
        shrink_frame = np.zeros([_sX,_sY])
        for i in range(_sX):
            for j in range(_sY):
                shrink_frame[i][j] = sum(frame[i*shrink_size:(i+1)*shrink_size,j*shrink_size:(j+1)*shrink_size].flatten()) / (shrink_size*shrink_size)
        return shrink_frame.astype(frame.dtype)
    return np.array(map(func, img_stack))

@exeTime
def projection(img_stack, method='max'):
    if method == 'max':
        proj = np.max(img_stack, axis=0)
    elif method == 'min':
        proj = np.min(img_stack, axis=0)
    elif method == 'mean':
        proj = np.mean(img_stack, axis=0)
    else:
        raise "Bad Projection Method", method
    return proj

def smooth(img_stack, smooth_size):
    from skimage.filters import rank
    from skimage.morphology import disk
    def func(frame):
        smoothed = rank.median(frame,disk(smooth_size))
        smoothed = rank.enhance_contrast(smoothed, disk(smooth_size))
        return smoothed
    return np.array(map(func,img_stack))

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

