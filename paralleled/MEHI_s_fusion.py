################################
# Author   : septicmk
# Date     : 2015/4/12 19:13:28
# FileName : MEHI_fusion.py
################################

import skimage.external.tifffile as tiff
import skimage.morphology as mor
from skimage.filters import gaussian_filter
from skimage import img_as_float
import numpy as np
import math
from MEHI_s_common import *
import MEHI_s_tool as IO_tool
#import cPickle as pickle

class Fusion:
    
    # 2-side fusion 
    def kernel(self, img_stack, x, y, z, wsize):
        a = []
        _Z, _X, _Y, = img_stack.shape
        # for test
        for iz in range(-1, 1):
            for ix in range(-wsize, wsize):
                for iy in range(-wsize, wsize):
                    a.append(img_stack[abs(z+iz) if abs(z+iz) < _Z else 2*_Z - abs(z+iz) - 1][abs(x+ix) if abs(x+ix) < _X else _X*2 - abs(x+ix) - 1][abs(y+iy) if abs(y+iy) < _Y else 2*_Y - abs(y+iy) - 1])
        return np.array(a)
                    
    @exeTime
    def entropy(self, img_stack, wsize, bins):
        ent_mat = np.zeros_like(img_stack).astype(float)
        _Z, _X, _Y, = img_stack.shape
        for z in range(_Z):
            for x in range(_X):
                print "* (%d,%d)" % (z,x)
                for y in range(_Y):
                    tmp = self.kernel(img_stack, x, y, z, wsize)
                    hist, edge = np.histogram(tmp, bins, density=True)
                    hist = map(lambda x : x*math.log(x,2) if x > 0 else 0, hist)
                    ent_mat[z][x][y] = -sum(hist)
        return ent_mat
   
    @exeTime   
    def fusion(self, img_stack_A, img_stack_B, wsize ,bins):
        ent_mat_A = self.entropy(img_stack_A, wsize, bins)
        ent_mat_B = self.entropy(img_stack_B, wsize, bins)
        fused_img = np.zeros_like(img_stack_A)
        fused_img = img_stack_A*ent_mat_A + img_stack_B*ent_mat_B
        fused_img = fused_img / (ent_mat_A + ent_mat_B) 
        fused_img = fused_img.astype(np.uint8)
        return fused_img
    
    @exeTime
    def q_fusion(self, rdd, sgm1, sgm2): 
        '''
        Usage:
         - a fast implementation of fusion
        Args:
         - rdd: the ziped L&R img stack
         - sgm1/sgm2: just leave it alone
        '''
        def func(dframe):
            frame1, frame2 = dframe[0], dframe[1]
            tmp1 = frame1 - gaussian_filter(frame1,sgm1)
            tmp1 = gaussian_filter(tmp1*tmp1,sgm2)
            tmp2 = frame2 - gaussian_filter(frame2,sgm1)
            tmp2 = gaussian_filter(tmp2*tmp2,sgm2)
            return (tmp1*frame1 + frame1*tmp1)/(tmp1+tmp2)
        log('info')('fusing start\n')
        rdd = rdd.map(func)
        fused_img = np.array(rdd.collect())
        fused_img = fused_img.astype(np.uint8)
        log('info')('fusing success\n')
        return fused_img
    
if __name__ == '__main__':
    pass
