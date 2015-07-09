################################
# Author   : septicmk
# Date     : 2015/3/21 17:24:50
# FileName : MEHI_preprocess.py
################################

import skimage.external.tifffile as tiff
import skimage.morphology as mor
from skimage.filters import gaussian_filter
from skimage import img_as_float
import numpy as np
import math
from MEHI_s_common import *

class Preprocess:

    @exeTime
    def stripe_removal(self, rdd):
        '''
        Usage:
         - remove the stripe
         - (discarded)
        '''
        def func(frame):
            kernel = nor.disk(3)
            frameWP = frame - mor.white_tophat(frame, kernel) * (mor.white_tophat(frame, kernel) > 1000).astype(float)
            kernel = mor.rectangle(25, 1)
            closed = mor.closing(frameWP, kernel)
            opened = mor.opening(closed, kernel)
            result = ((frameWP.astype(float) / opened.astype(float)) * 3000.0)
            return result.astype(int)
        return rdd.map(func)
   
    @exeTime
    def intensity_normalization(self, rdd, num):
        '''
        Usage:
         - adjust the intensity
        args:
         - num: if you wanna 16-bit output, just let num = 16
        '''
        def func(frame):
            max_intensity = max(frame.flatten())
            min_intensity = min(frame.flatten())
            return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*255, frame)).astype(np.uint8)
        def func2(frame):
            max_intensity = max(frame.flatten())
            min_intensity = min(frame.flatten())
            return np.array(map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*65535, frame)).astype(np.uint16)
        if num == 8:
            return rdd.map(func)
        elif num == 16:
            return rdd.map(func2)
        else: 
            return rdd
    
    @exeTime
    def flip(self, rdd):
        def func(frame):
            return frame[:,::-1]
        return rdd.map(func)
        
    @exeTime 
    def invert(self, rdd):
        def func(frame):
            return map(lambda p: 255-p, frame)
        return rdd.map(func)
    
    @exeTime
    def sub_background(self, rdd):
        def func(frame):
            return mor.black_tophat(frame, mor.disk(15))
        return rdd.map(func)
        
if __name__ == '__main__':
    print 'OK'
    pass

