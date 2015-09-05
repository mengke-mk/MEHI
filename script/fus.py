################################
# Author   : septicmk
# Date     : 2015/08/12 14:04:49
# FileName : fus.py
################################

from MEHI.paralleled import preprocess as prep
from MEHI.paralleled import registration as reg
from MEHI.paralleled import fusion as fus
from MEHI.serial import preprocess as _prep
from MEHI.paralleled import IO
from pyspark import SparkContext, SparkConf
from MEHI.utils.tool import exeTime, log
import numpy as np
import time

conf = SparkConf().setAppName('fuse').setMaster('local[128]').set('spark.executor.memory','20g').set('spark.driver.maxResultSize','20g').set('spark.driver.memory','40g').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2').set('spark.default.parallelism','512')
sc = SparkContext(conf=conf)

pwd = '/mnt/xfs_snode21'
s = time.time()

s_loading = time.time()
log('info')('loading tiff ...')
L_img_stack = IO.load_tiff(sc, pwd+'/0401RawData/1-L-Red')
R_img_stack = IO.load_tiff(sc, pwd+'/0401RawData/1-R-Red')
rddA = sc.parallelize(L_img_stack)
rddB = sc.parallelize(R_img_stack)
e_loading = time.time()
log('time')('loading cost %.3f' % (e_loading-s_loading))
log('info')('tiff load over...')


log('info')('registration start ...')
s_reg = time.time()
rddA = prep.intensity_normalization(rddA,8)
rddB = prep.intensity_normalization(rddB,8)
rddB = prep.flip(rddB)
L_img_stack_8 = np.array(rddA.collect())
R_img_stack_8 = np.array(rddB.collect())
e_pre = time.time()
log('time')('preprocess cost %.3f' % (e_pre-s_reg))
vec0 = [0,0,0,1,1,0,0]
vec = reg.c_powell(L_img_stack_8[233], R_img_stack_8[233], vec0)
rddB = sc.parallelize(R_img_stack)
rddB = prep.flip(rddB)
rddB = reg.execute(rddB, vec) 
R_img_stack = rddB.collect()
e_reg = time.time()
log('time')('registration cost %.3f' % (e_reg-s_reg))
log('info')('registration over ...')

log('info')('fuion start ...')
s_fus = time.time()
R_img_stack = np.squeeze(np.array(R_img_stack))
img_stack = zip(L_img_stack, R_img_stack)
rdd = sc.parallelize(img_stack)
fused_img = fus.wavelet_fusion(rdd)
e_fus = time.time()
log('time')('fusion cost %.3f' % (e_fus-s_fus))
log('info')('fusion over ...')

#log('info')('saving ...') 
#IO.save_tiff(fused_img, pwd+'/0401fusion/fus_dev/fus') 
#log('info')('subtract background start ...')

s_sub = time.time()
fused_img = IO.load_tiff(sc ,pwd+'/0401fusion/fus_dev')
rdd = sc.parallelize(fused_img)
rdd = prep.intensity_normalization(rdd)
rdd = prep.subtract_Background(rdd)
rdd = prep.intensity_normalization(rdd)
sb_img = np.array(rdd.collect())
e_sub = time.time()
log('time')('sub_prep cost %.3f' % (e_sub-s_sub))
log('info')('sbutract background over ... ')
#
#log('info')('saving ...')
#IO.save_tiff(sb_img, pwd+'/0401fusion/sub_dev/sub')
sc.stop()
e = time.time()
print "[info] %.3f s" %(e-s)
