################################
# Author   : septicmk
# Date     : 2015/07/23 18:14:26
# FileName : preprocess.py
################################

import skimage.external.tifffile as tiff
import numpy as np
import math

def stripe_removal(rdd):
    '''
    Usage:
     - remove the stripe
     - (discarded)
    '''
    import skimage.morphology as mor
    def func(frame):
        _dtype = frame.dtype
        kernel = nor.disk(3)
        frameWP = frame - mor.white_tophat(frame, kernel) * (mor.white_tophat(frame, kernel) > 1000).astype(float)
        kernel = mor.rectangle(25, 1)
        closed = mor.closing(frameWP, kernel)
        opened = mor.opening(closed, kernel)
        result = ((frameWP.astype(float) / opened.astype(float)) * 3000.0)
        return result.astype(_dtype)
    return rdd.map(func)

def intensity_normalization(rdd, dtype=None):
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
        return rdd.map(func8)
    elif dtype == 16:
        return rdd.map(func16)
    else:
        return rdd.map(funca)

def flip(rdd):
    def func(frame):
        return frame[:,::-1]
    return rdd.map(func)
    
def invert(rdd):
    def func(frame):
        if frame.dtype == np.uint8:
            return map(lambda p: 255-p, frame)
        elif frame.dtype == np.uint16:
            return map(lambda p: 65535-p, frame)
        else :
            return map(lambda p: p, frame)
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

def subtract_Background(rdd, size=10):
    '''
    Usage:
     - subtrackt Background (based on C)
    args:
     - radius: the smooth size
    '''
    from MEHI.udf.SB import subtract_Background
    def func(frame):
        return subtract_Background(frame, size)
    return rdd.map(func)
        
if __name__ == '__main__':
    print 'OK'
    pass

