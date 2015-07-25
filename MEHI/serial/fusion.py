################################
# Author   : septicmk
# Date     : 2015/07/23 20:10:31
# FileName : fusion.py
################################

import numpy as np
from MEHI.utils.tool import exeTime
import math

@exeTime
def content_fusion(img_stack, sgm1=44, sgm2=81): 
    '''
    Usage:
     - a fast implementation of content-based fusion
    Args:
     - rdd: the ziped L&R img stack
     - sgm1/sgm2: gaussian smooth size
    '''
    from skimage.filters import gaussian_filter
    def func(dframe):
        frame1, frame2 = dframe[0], dframe[1]
        tmp1 = frame1 - gaussian_filter(frame1,sgm1)
        tmp1 = gaussian_filter(tmp1*tmp1,sgm2)
        tmp2 = frame2 - gaussian_filter(frame2,sgm1)
        tmp2 = gaussian_filter(tmp2*tmp2,sgm2)
        ret = (tmp1*frame1 + frame1*tmp1)/(tmp1+tmp2)
        ret = ret.astype(frame1.dtype)
        return ret
    fused_img = np.array(map(func, img_stack))
    return fused_img

@exeTime
def wavelet_fusion(img_stack, level=5):
    '''
    Usage:
     - a implementation of wavelet fusion (C based)
    Args:
     - level: wavelet level
    '''
    import pywt
    def fuse(A, C, S):
        T = [A]
        for c, s in zip(C, S):
            cH,cV,cD = c
            sH,sV,sD = s
            tH = map(lambda x,y: map(lambda a,b: a if abs(a) > abs(b) else b, x,y), cH, sH)
            tV = map(lambda x,y: map(lambda a,b: a if abs(a) > abs(b) else b, x,y), cV, sV)
            tD = map(lambda x,y: map(lambda a,b: a if abs(a) > abs(b) else b, x,y), cD, sD)
            T.append((tH,tV,tD))
        return T
    def func(dframe):
        frame1, frame2 = dframe[0], dframe[1]
        frame1 = np.array(frame1)
        frame2 = np.array(frame2)
        C = pywt.wavedec2(frame1, 'db4', level=level)
        S = pywt.wavedec2(frame2, 'db4', level=level)
        tA2 = (C[0] + S[0])/2
        coeffs = fuse(tA2, C[1:], S[1:])
        fuse_img = pywt.waverec2(coeffs, 'db4')
        if frame1.dtype == np.uint16:
            fuse_img = fuse_img.clip(0,65535).astype(np.uint16)
        elif frame1.dtype == np.uint8:
            fuse_img = fuse_img.clip(0,255).astype(np.uint8)
        return fuse_img
    fused_img = np.array(map(func, img_stack))
    fused_img = fused_img.astype(fused_img[0].dtype)
    return fused_img
    
if __name__ == '__main__':
    pass
