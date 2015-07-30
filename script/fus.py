################################
# Author   : septicmk
# Date     : 2015/07/25 16:14:09
# FileName : main.py
################################

from MEHI.paralleled import preprocess as prep
from MEHI.paralleled import registration as reg
from MEHI.paralleled import fusion as fus
from MEHI.serial import preprocess as _prep
from MEHI.serial import IO
from pyspark import SparkContext, SparkConf
from MEHI.utils.tool import exeTime, log
import numpy as np
import time

conf = SparkConf().setAppName('test').setMaster('local[48]').set('spark.executor.memory','20g').set('spark.driver.maxResultSize','20g').set('spark.driver.memory','40g').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2').set('spark.default.parallelism','128')
sc = SparkContext(conf=conf)

pwd = '/mnt/md_5T/Galaxy_inst/pku_Galaxy/galaxy/database/ftp/liuyao@ncic.ac.cn'
s = time.time()
log('info')('loading tiff ...')
L_img_stack = IO.load_tiff(pwd+'/0401RawData/1-L-Red')
R_img_stack = IO.load_tiff(pwd+'/0401RawData/1-R-Red')
rddA = sc.parallelize(L_img_stack)
rddB = sc.parallelize(R_img_stack)
log('info')('tiff load over...')


log('info')('registration start ...')
rddA = prep.intensity_normalization(rddA,8)
rddB = prep.intensity_normalization(rddB,8)
rddB = prep.flip(rddB)
L_img_stack_8 = np.array(rddA.collect())
R_img_stack_8 = np.array(rddB.collect())
vec0 = [0,0,0,1,1,0,0]
vec = reg.c_powell(L_img_stack_8[233], R_img_stack_8[233], vec0)
rddB = sc.parallelize(R_img_stack)
rddB = prep.flip(rddB)
rddB = reg.execute(rddB, vec) 
R_img_stack = rddB.collect()
log('info')('registration over ...')

log('info')('fuion start ...')
R_img_stack = np.squeeze(np.array(R_img_stack))
img_stack = zip(L_img_stack, R_img_stack)
rdd = sc.parallelize(img_stack)
fused_img = fus.wavelet_fusion(rdd)
log('info')('fusion over ...')

log('info')('saving ...')
IO.save_tiff(fused_img, pwd+'/0401fusion/fus_dev/fus')

#log('info')('subtract background start ...')
#fused_img = IO.load_tiff(pwd+'/0401fusion/fus_dev')
#rdd = sc.parallelize(fused_img)
#rdd = prep.intensity_normalization(rdd)
#rdd = prep.subtract_Background(rdd)
#rdd = prep.intensity_normalization(rdd)
#sb_img = np.array(rdd.collect())
#log('info')('sbutract background over ... ')
#
#log('info')('saving ...')
#IO.save_tiff(sb_img, pwd+'/0401fusion/sub_dev/sub')
sc.stop()
e = time.time()
print "[info] %.3f s" %(e-s)
