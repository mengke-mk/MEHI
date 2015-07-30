################################
# Author   : septicmk
# Date     : 2015/07/23 20:10:23
# FileName : preprocess.py
################################

import skimage.external.tifffile as tiff
import numpy as np
import math
from MEHI.utils.tool import exeTime

@exeTime
def stripe_removal(img_stack):
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
    return np.array(map(func, img_stack)).astype(img_stack[0].dtype)

@exeTime
def intensity_normalization(img_stack, dtype=None):
    '''
    Usage:
     - adjust the intensity
    args:
     - num: if you wanna 16-bit output, just let num = 16,  
    '''
    def func8(frame):
        max_intensity = max(frame.flatten())
        min_intensity = min(frame.flatten())
        return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*255, frame)).astype(np.uint8)
    def func16(frame):
        max_intensity = max(frame.flatten())
        min_intensity = min(frame.flatten())
        return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*65535, frame)).astype(np.uint16)
    def funca(frame):
        max_intensity = max(frame.flatten())
        min_intensity = min(frame.flatten())
        if frame.dtype == np.uint8:
            return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*255, frame)).astype(np.uint8)
        else:
            return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*65535, frame)).astype(np.uint16)
    if dtype == 8:
        return np.array(map(func8, img_stack)).astype(np.uint8)
    elif dtype == 16:
        return np.array(map(func16, img_stack)).astype(np.uint16)
    else:
        return np.array(map(funca, img_stack)).astype(img_stack[0].dtype)

@exeTime
def flip(img_stack):
    def func(frame):
        return frame[:,::-1]
    return np.array(map(func,img_stack))
    
@exeTime
def invert(img_stack):
    def func(frame):
        if frame.dtype == np.uint8:
            return map(lambda p: 255-p, frame)
        elif frame.dtype == np.uint16:
            return map(lambda p: 65535-p, frame)
        else :
            return map(lambda p: p, frame)
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


        
if __name__ == '__main__':
    print 'OK'
    pass

