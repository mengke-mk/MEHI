################################
# Author   : septicmk
# Date     : 2015/4/6 18:52:10
# FileName : MEHI_main.py
################################

import MEHI_s_tool
import MEHI_s_preprocess
import MEHI_s_registration
import MEHI_s_fusion
import MEHI_s_segmentation
import MEHI_s_filter
import traceback
import numpy as np
from MEHI_s_global import *
from MEHI_s_common import *

IO_tool = MEHI_s_tool.Img_IO()
prep = MEHI_s_preprocess.Preprocess()
reg = MEHI_s_registration.Registration()
fus = MEHI_s_fusion.Fusion()
seg = MEHI_s_segmentation.Segmentation()
spftr = MEHI_s_filter.Spatial_Filter()

if __name__ == '__main__':
    conf = SparkConf().setAppName('MEHI').setMaster('local[16]').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2')
    sc = SparkContext(conf=conf)
    
    @exeTime
    def init():
        L_img_stack = IO_tool.read(left_pwd)
        R_img_stack = IO_tool.read(right_pwd)
	print left_pwd
        msg = 'len(L)= %d, len(R)= %d\n' %(len(L_img_stack), len(R_img_stack))
        log('info')(msg)
        return L_img_stack, R_img_stack
    
    @exeTime
    def preprocess(L_img_stack, R_img_stack, num):
        rddA = sc.parallelize(L_img_stack, 64)
        rddB = sc.parallelize(R_img_stack, 64)
        if num == 16:    
            rddA = prep.intensity_normalization(rddA, 16)
            rddB = prep.flip(rddB)
            rddB = prep.intensity_normalization(rddB, 16)
        if num == 8:
            rddA = prep.intensity_normalization(rddA, 8)
            rddA = prep.sub_background(rddA) 
            rddB = prep.intensity_normalization(rddB, 8)
            rddB = prep.sub_background(rddB)
            rddB = prep.flip(rddB)
        return rddA, rddB

    @exeTime
    def registration(rddA, rddB, conf=0):
        if conf == 0:
            vec=[ 26.09463356, -5.22590429, 3.16175216, 5.49837414, 5.49837414, 4.49837414, 4.49837414 ]
            rddB = reg.execute(rddB, vec)
            return rddB
        else:
            vec0 = [0,0,0,1,1,0,0]
            L_img_stack = rddA.collect()
	    R_img_stack = rddB.collect()
            vec = reg.q_powell(L_img_stack[sample_index], R_img_stack[sample_index], vec0)
            open('logvec.txt','w').write(str(vec))
            rddB = reg.execute(rddB, vec)
            return rddB
    
    @exeTime
    def fusion(rddA, rddB):
        img_stack_A = np.array(rddA.collect())
        img_stack_B = np.array(rddB.collect())
        img_stack = zip(img_stack_A, img_stack_B)
        log('info')('mark')
        rdd = sc.parallelize(img_stack, 64)
        fuse_img = fus.q_fusion(rdd, sgm1, sgm2)
        #IO_tool.write("fuse_img.tif", fuse_img) 
        return fuse_img
    
    @exeTime
    def segmentation(fuse_img):
        rdd = sc.parallelize(fuse_img,64)
        seg.main(fuse_img, rdd)
###
    L_img_stack, R_img_stack = init()
    rddA, rddB = preprocess(L_img_stack, R_img_stack, 16)
    #rddB = registration(rddA, rddB, conf=1)
    fuse_img = fusion(rddA, rddB)
        
