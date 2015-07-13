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
from MEHI_common import *
from MEHI_tool import *

class Preprocess:

    @exeTime 
    def stripe_removal(self, img_stack):
        '''
        Usage:
         - remove the stripe
         - (discarded)
        '''
        img = self.img
        ret = np.empty_like(img)
        for z, frame in enumerate(img):
            #if z > 10: break
            msg = "stripe_removal %d-th frame" % (z+1)
            end = len(img)
            bar('info')(msg, z+1, end)
            kernel = mor.disk(3)
            frameWP = frame - mor.white_tophat(frame, kernel) * (mor.white_tophat(frame, kernel) > 1000).astype(float)
            kernel = mor.rectangle(25, 1)
            closed = mor.closing(frameWP, kernel)
            opened = mor.opening(closed, kernel)
            result = ((frameWP.astype(float) / opened.astype(float)) * 3000.0)
            ret[z] = result.astype(int) 
        return ret
    
    @exeTime
    def intensity_normalization(self, img_stack, num):
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
        # max_intensity = 0
        # min_intensity = 0
        ret = np.zeros_like(img_stack)
        for z, frame in enumerate(img_stack):
            msg = "intensity_normalisztion %d-th frame" % (z+1)
            end = len(img_stack)
            bar('info')(msg, z+1, end)
            #max_intensity = max(frame.flatten()) 
            #min_intensity = min(frame.flatten())
            #ret[z] = map(lambda x: ((x-min_intensity+.0)/(max_intensity - min_intensity))*255, frame)
            if num  == 8:
	        ret[z] = func(frame)
	    elif num == 16:
	        ret[z] = func2(frame)
	    #log('debug')(str(ret[z].max()))
        #ret = ret.astype(np.uint8)
	if num == 8:
           return ret.astype(np.uint8)
	elif num == 16:
	   return ret.astype(np.uint16)
    
    @exeTime
    def flip(self, img_stack):
        return img_stack[:,:,::-1]

    @exeTime
    def invert(self, img_stack):
        ret = np.zeros_like(img_stack)
        for j in range(len(img_stack)):
            ret[j] = map(lambda x: 255-x, img_stack[j])
        return ret
    
    @exeTime
    def sub_background(self, img_stack):
        ret = np.zeros_like(img_stack)
        for z, frame in enumerate(img_stack):
	   msg = "sub_background %d-th frame" % (z+1)
	   end = len(img_stack)
	   bar('info')(msg, z+1, end)
           ret[z] = mor.black_tophat(frame, mor.disk(10))
        return ret
        
if __name__ == '__main__':
    IO = MEHI_Tool()
    pass

