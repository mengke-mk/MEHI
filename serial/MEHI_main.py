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
from MEHI_global import *
from MEHI_common import *

if __name__ == '__main__':
    IO_tool = MEHI_tool.Img_IO()
    prep = MEHI_preprocess.Preprocess()
    reg = MEHI_registration.Registration()
    fus = MEHI_fusion.Fusion()
    seg = MEHI_segmentation.Segmentation()
    spftr = MEHI_filter.Spatial_Filter()
    
    def init():
        L_img_stack = IO_tool.read(left_pwd)
        R_img_stack = IO_tool.read(right_pwd)
        msg = 'len(L)= %d, len(R)= %d\n' %(len(L_img_stack), len(R_img_stack))
        log('info')(msg)
        return L_img_stack, R_img_stack
    
    def preprocess():
        L_img_stack = IO_tool.read(left_pwd) 
        R_img_stack = IO_tool.read(right_pwd)
        L_img_stack = prep.intensity_normalization(L_img_stack)
        R_img_stack = prep.intensity_normalization(R_img_stack)
        R_img_stack = prep.flip(R_img_stack)
        R_img_stack = prep.sub_background(R_img_stack)
        return L_img_stack, R_img_stack
    
    def registration(L_img_stack, R_img_stack, conf=0):
        if conf == 0:
            vec=[ -4.47617039e-01, 1.51950091e+01, 3.89617141e-03, 9.98441922e-01, 9.94042566e-01, 2.24870341e-05, 3.14704115e-03]
            R_img_stack = reg.execute(R_img_stack, vec)
            return R_img_stack
        else:
            vec0 = np.array([2, 15, 0, 1, 1, 0 ,0])
            vec = reg.q_powell(L_img_stack[sample_index], R_img_stack[sample_index], vec0)
            R_img_stack = reg.execute(R_img_stack, vec)
            return R_img_stack
   
    def fusion_16(L_img_stack, R_img_stack):
        L_img_stack = IO_tool.readone('L_reg_img_stack.tif')
        R_img_stack = IO_tool.readone('R_reg_img_stack.tif')
        L_img_stack = L_img_stack[0:125]
        R_img_stack = R_img_stack[0:125]
        fuse_img = fus.q_fusion(L_img_stack, R_img_stack, sgm1, sgm2)
        IO_tool.write('fuse_img_show_stack_v1.tif',fuse_img)
       
        L_img_stack = IO_tool.readone('L_reg_img_stack.tif')
        R_img_stack = IO_tool.readone('R_reg_img_stack.tif')
        L_img_stack = L_img_stack[125:250]
        R_img_stack = R_img_stack[125:250]
        fuse_img = fus.q_fusion(L_img_stack, R_img_stack, sgm1, sgm2)
        IO_tool.write('fuse_img_show_stack_v2.tif',fuse_img)
       
        L_img_stack = IO_tool.readone('L_reg_img_stack.tif')
        R_img_stack = IO_tool.readone('R_reg_img_stack.tif')
        L_img_stack = L_img_stack[250:375]
        R_img_stack = R_img_stack[250:375]
        fuse_img = fus.q_fusion(L_img_stack, R_img_stack, sgm1, sgm2)
        IO_tool.write('fuse_img_show_stack_v3.tif',fuse_img)
       
        L_img_stack = IO_tool.readone('L_reg_img_stack.tif')
        R_img_stack = IO_tool.readone('R_reg_img_stack.tif')
        L_img_stack = L_img_stack[375:500]
        R_img_stack = R_img_stack[375:500]
        fuse_img = fus.q_fusion(L_img_stack, R_img_stack, sgm1, sgm2)
        IO_tool.write('fuse_img_show_stack_v4.tif',fuse_img)
    
        L_img_stack = IO_tool.readone('fuse_img_show_stack_v1.tif')
        R_img_stack = IO_tool.readone('fuse_img_show_stack_v2.tif')
        fuse_img = np.concatenate((L_img_stack, R_img_stack), axis=0)
        IO_tool.write('fuse_img_show_stack_v1.tif',fuse_img)
        L_img_stack = IO_tool.readone('fuse_img_show_stack_v3.tif')
        R_img_stack = IO_tool.readone('fuse_img_show_stack_v4.tif')
        fuse_img = np.concatenate((L_img_stack, R_img_stack), axis=0)
        IO_tool.write('fuse_img_show_stack_v2.tif',fuse_img)
        L_img_stack = IO_tool.readone('fuse_img_show_stack_v1.tif')
        R_img_stack = IO_tool.readone('fuse_img_show_stack_v2.tif')
        fuse_img = np.concatenate((L_img_stack, R_img_stack), axis=0)
        IO_tool.write('fuse_img_show_stack.tif',fuse_img)
     
    def fusion_8(L_img_stack, R_img_stack):
        L_img_stack = IO_tool.readone('L_reg_img_stack_8bit.tif')
        R_img_stack = IO_tool.readone('R_reg_img_stack_8bit.tif')
        L_img_stack = L_img_stack[0:250]
        R_img_stack = R_img_stack[0:250]
        fuse_img = fus.q_fusion(L_img_stack, R_img_stack, sgm1, sgm2)
        IO_tool.write('fuse_img_seg_stack_v1.tif',fuse_img)
       
        L_img_stack = IO_tool.readone('L_reg_img_stack_8bit.tif')
        R_img_stack = IO_tool.readone('R_reg_img_stack_8bit.tif')
        L_img_stack = L_img_stack[250:500]
        R_img_stack = R_img_stack[250:500]
        fuse_img = fus.q_fusion(L_img_stack, R_img_stack, sgm1, sgm2)
        IO_tool.write('fuse_img_seg_stack_v2.tif',fuse_img)
       
        L_img_stack = IO_tool.readone('fuse_img_seg_stack_v1.tif')
        R_img_stack = IO_tool.readone('fuse_img_seg_stack_v2.tif')
        fuse_img = np.concatenate((L_img_stack, R_img_stack), axis=0)
        IO_tool.write('fuse_img_seg_stack.tif',fuse_img)
   
    def segmentation():  
        img_stack = IO_tool.readone('fuse_img_seg_stack.tif')
        seg.main(img_stack)
#########################################
    L_img_stack, R_img_stack = init()
