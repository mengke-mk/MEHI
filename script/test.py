################################
# Author   : septicmk
# Date     : 2015/08/17 11:13:23
# FileName : test.py
################################

from MEHI.paralleled import preprocess as prep
from MEHI.paralleled import segmentation as seg
from MEHI.paralleled import IO
from MEHI.utils.tool import exeTime, log
from pyspark import SparkContext, SparkConf
import numpy as np
import time

conf = SparkConf().setAppName('seg').setMaster('local[128]').set('spark.executor.memory','20g').set('spark.driver.maxResultSize','20g').set('spark.driver.memory','40g').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2').set('spark.default.parallelism','256')

sc = SparkContext(conf=conf)

pwd = '/mnt/xfs_snode21/0401fusion'
s = time.time()

log('info')('load tiff ...')
fus = IO.load_tiff(sc, pwd+'/fus_dev/')
log('info')('tiff load over ...')

ret = []
for y in range(fus.shape[1]):
    t = fus[:,y,:]
    ret.append(t)

ret = np.array(ret)
IO.save_tiff(ret, pwd+'/yz/yz')



sc.stop()
e = time.time()
log('time')("%.3f s in total." % (e-s))

