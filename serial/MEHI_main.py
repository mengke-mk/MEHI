################################
# Author   : septicmk
# Date     : 2015/4/6 18:52:10
# FileName : MEHI_main.py
################################

import MEHI_tool
import MEHI_preprocess
import MEHI_registration
import MEHI_fusion
import MEHI_segmentation
import MEHI_filter
import traceback
import numpy as np
import os
import multiprocessing as mul
from MEHI_global import *
from MEHI_common import *

IO_tool = MEHI_tool.Img_IO()
prep = MEHI_preprocess.Preprocess()
reg = MEHI_registration.Registration()
fus = MEHI_fusion.Fusion()
seg = MEHI_segmentation.Segmentation()
spftr = MEHI_filter.Spatial_Filter()

@exeTime
def init(left_pwd, right_pwd):
    L_img_stack = IO_tool.read(left_pwd)
    R_img_stack = IO_tool.read(right_pwd)
    msg = 'len(L)= %d, len(R)= %d\n' %(len(L_img_stack), len(R_img_stack))
    log('info')(msg)
    #L_img_stack = np.array(L_img_stack).astype(np.uint16)
    #R_img_stack = np.array(R_img_stack).astype(np.uint16)
    return L_img_stack, R_img_stack

@exeTime
def preprocess(L_img_stack, R_img_stack, num):
    #L_img_stack = IO_tool.read(left_pwd) 
    #R_img_stack = IO_tool.read(right_pwd)
    L_img_stack = prep.intensity_normalization(L_img_stack, num)
    R_img_stack = prep.intensity_normalization(R_img_stack, num)    
    if num == 8:
        R_img_stack = prep.sub_background(R_img_stack)
        L_img_stack = prep.sub_background(L_img_stack)
    R_img_stack = prep.flip(R_img_stack)
    return L_img_stack, R_img_stack

@exeTime 
def registration(L_img_stack, R_img_stack, conf=0):
    if conf == 0:
        vec=[4.93240264e+04, 4.42055684e+01, 1.94141852e+01, 3.02055684e+01, -1.28626769e+01,  2.92055684e+01, 2.92055684e+01]
        R_img_stack = reg.execute(R_img_stack, vec)
        return R_img_stack
    else:
        vec0 = np.array([2, 15, 0, 1, 1, 0 ,0])
        sample_index = reg.match(L_img_stack, R_img_stack)
        vec = reg.q_powell(L_img_stack[sample_index], R_img_stack[sample_index], vec0)
        R_img_stack = reg.execute(R_img_stack, vec)
        return R_img_stack

@exeTime
def fusion_small(L_img_stack, R_img_stack):
    #L_img_stack = IO_tool.readone('l.tif')
    #R_img_stack = IO_tool.readone('r.tif')
    #L_img_stack = L_img_stack[0:len(L_img_stack)]
    #R_img_stack = R_img_stack[0:len(R_img_stack)]
    L_img_stack = np.array(L_img_stack).astype(np.uint16)
    R_img_stack = np.array(R_img_stack).astype(np.uint16)
    fuse_img = fus.q_fusion(L_img_stack, R_img_stack, sgm1, sgm2)
    IO_tool.write('fuse_img_seg_stack_small_4.tif',fuse_img)

@exeTime
def fusion(L_img_stack, R_img_stack, tp):
    L_img_stack = np.array(L_img_stack).astype(np.uint16)
    R_img_stack = np.array(R_img_stack).astype(np.uint16)
    n, s = len(L_img_stack), 0
    while n > s:
        L_, R_ = [], []
        if n > s+100:
            L_, R_ = L_img_stack[s:s+100], R_img_stack[s:s+100]
        else:
            L_, R_ = L_img_stack[s:n], R_img_stack[s:n]
        fuse_img = fus.q_fusion(L_, R_, sgm1, sgm2)
        IO_tool.write2f('/'+str(tp)+'/fus', fuse_img, offset=s)
        s += 100

def segmentation():  
    img_stack = IO_tool.readone('fuse_img_seg_stack.tif')
    seg.main(img_stack)

def udf(img_pwd):
    tp = os.path.split(img_pwd[0])[1]
    L_img_stack, R_img_stack = init(img_pwd[0], img_pwd[1])
    L_img_stack, R_img_stack = preprocess(L_img_stack, R_img_stack, 16)
    R_img_stack = registration(L_img_stack, R_img_stack, conf=0)
    #fusion_small(L_img_stack, R_img_stack)
    fusion(L_img_stack, R_img_stack, tp)

#########################################
if __name__ == '__main__':
    inputs = [img for img in IO_tool.input(img_pwd)]
    pool = mul.Pool(16)
    pool.map(udf, inputs)
    pool.close()
    pool.join()
    
