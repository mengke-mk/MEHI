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
    
    @exeTime
    def init():
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
	#L_img_stack = prep.invert(L_img_stack)
	#R_img_stack = prep.invert(R_img_stack)
        R_img_stack = prep.sub_background(R_img_stack)
        L_img_stack = prep.sub_background(L_img_stack)
	R_img_stack = prep.flip(R_img_stack)
	IO_tool.write2f('/preprocess_L'+str(num)+'bit/preprocess', L_img_stack)
	IO_tool.write2f('/preprocess_R'+str(num)+'bit/preprocess', R_img_stack)
	return L_img_stack, R_img_stack

    @exeTime 
    def registration(L_img_stack, R_img_stack, conf=0):
        if conf == 0:
	    # Data 1
            vec=[-4.47617039e-01, 1.51950091e+01, 3.89617141e-03, 9.98441922e-01 , 9.94042566e-01, 2.24870341e-05, 3.14704115e-03]
            # Data 2
	    #vec=[-3.04981490e+01, 4.38364719e+01, 4.24726430e+00, 2.82550778e-02, 3.31111499e-01, 9.39129920e-01, 3.21995247e-01]
	    R_img_stack = reg.execute(R_img_stack, vec)
	    IO_tool.write2f('/registration_R8bit/reg', R_img_stack)
            return R_img_stack
        else:
            vec0 = np.array([2, 15, 0, 1, 1, 0 ,0])
            #`sample_index = reg.match(L_img_stack, R_img_stack)
	    vec = reg.q_powell(L_img_stack[sample_index], R_img_stack[sample_index], vec0)
            open('E75D1B8vec0627.txt','w').write(str(vec))
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
   
    @exeTime
    def fusion_small(L_img_stack, R_img_stack, num):
	#L_img_stack = IO_tool.readone('l.tif')
	#R_img_stack = IO_tool.readone('r.tif')
        #L_img_stack = L_img_stack[0:len(L_img_stack)]
        #R_img_stack = R_img_stack[0:len(R_img_stack)]
	if num == 16:
            L_img_stack = np.array(L_img_stack).astype(np.uint16)
	    R_img_stack = np.array(R_img_stack).astype(np.uint16)
        elif num == 8:
	    L_img_stack = np.array(L_img_stack).astype(np.uint8)
	    R_img_stack = np.array(R_img_stack).astype(np.uint8)
	fuse_img = fus.q_fusion(L_img_stack, R_img_stack, sgm1, sgm2, num)
        #IO_tool.write('fuse_img_seg_stack_small_4.tif',fuse_img)
	IO_tool.write2f('/fusion'+str(num)+'bit/fus', fuse_img)
        return fuse_img

    @exeTime
    def segmentation(fuse_img):  
        #img_stack = IO_tool.readone('fuse_img_seg_stack.tif')
	#img_stack = IO_tool.read(output_pwd+'/fusion')
	#img_stack = IO_tool.read('/mnt/xfs_snode21/MEHI_DECONVOLUTION/20150401/E75/4/1-result-8bit')
	#img_stack = IO_tool.read('/mnt/xfs_snode21/MEHI_PROCESS_DATA/20150401/E75/4/1-Result/fusion8bit')
	#img_stack = np.array(img_stack, dtype=np.uint8)
        seg.main(fuse_img)
	####liuyao segment check 
	#img1 = IO_tool.readone('/mnt/xfs_snode21/MEHI_PROCESS_DATA/20150401/E75/4/1-Result/fusion8bit/fus_207.tif')
	#img1 = IO_tool.readone('/mnt/xfs_snode21/MEHI_Test_data/20150401sample/1-result-0625/fusion/fus_001.tif')
	#img1 = IO_tool.readone('/mnt/xfs_snode21/MEHI_PROCESS_DATA/20150401/E75/4/1-Result-0625serial/fusion8bit/fus_500.tif')
	#img1 = np.array(img1, dtype=np.uint8)
	#seg.check(img1)
#########################################
    #L_img_stack, R_img_stack = init()
    #L_img_stack, R_img_stack = preprocess(L_img_stack, R_img_stack, 8)
    #R_img_stack = registration(L_img_stack, R_img_stack, conf=0)
    #fuse_img = fusion_small(L_img_stack, R_img_stack, 8)
    #segmentation(fuse_img)
    L_img_stack = IO_tool.read(left_pwd)
    frame = L_img_stack[100]
    bin = seg.check(frame)
    bin = bin*255
    bin = np.array(bin,dtype=np.uint8)
    bin.astype(np.uint8)
    print bin.dtype, bin.max()
    IO_tool.write('test.tif', bin)
