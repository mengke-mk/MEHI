################################
# Author   : septicmk
# Date     : 2015/07/25 16:14:09
# FileName : main.py
################################

from MEHI.paralleled import preprocess as prep
from MEHI.paralleled import registration as reg
from MEHI.paralleled import fusion as fus
from MEHI.paralleled import IO
from pyspark import SparkContext, SparkConf
from MEHI.utils.tools import exeTime, log

conf = SparkConf().setAppName('test').setMaster('local[4]').set('spark.executor.memory','80g').set('spark.driver.maxResultSize','80g').set('spark.driver.memory','80g').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2').set('spark.default.parallelism','64')
sc = SparkContext(conf=conf)

pwd = '/mnt/md_5T/Galaxy_inst/pku_Galaxy/galaxy/database/ftp/liuyao@ncic.ac.cn'

L_img_stack = IO.load_tiff(sc, pwd+'/0401RawData/1-L-Red')
R_img_stack = IO.load_tiff(sc, pwd+'/0401RawData/1-R-Red')
log('info')('tiff load over...')

rddA = sc.parallelize(L_img_stack)
rddB = sc.parallelize(R_img_stack)

log('info')('intensity normalization start ...')
rddA = prep.intensity_normalization(rddA)
rddB = prep.intensity_normalization(rddB)
rddB = prep.flip(rddB)

_rddA = prep.intensity_normalization(rddA,8)
_rddB = prep.intensity_normalization(rddB,8)
log('info')('intensity normalization over ...')

log('info')('registration start ...')
L_img_stack_8 = np.array(_rddA.collect())
R_img_stack_8 = np.array(_rddA.collect())

vec0 = [0,0,0,1,1,0,0]
vec = reg.c_powell(L_img_stack_8[200], R_img_stack_8[200], vec0)
rddB = reg.execute(rddB, vec)
log('info')('registration over ...')

log('info')('fusion start ...')
L_img_stack = np.array(rddA.collect())
R_img_stack = np.array(rddB.collect())
img_stack = zip(L_img_stack, R_img_stack)
rdd = sc.parallelize(img_stack)
fused_img = fus.wavelet_fusion(rdd)
log('info')('fusion over ...')

log('info')('saving ...')
IO.save_tiff(fused_img, 'fus', pwd+'/0401fusion/')

log('info')('subtract background start ...')
rdd = sc.parallelize(fused_img)
sb_img = np.array(prep.subtract_Background(rdd).collect())
log('info')('sbutract background over ... ')

log('info')('saving ...')
IO.save_tiff(sb_img, 'sub', pwd+'/0401fusion/')



