################################
# Author   : septicmk
# Date     : 2015/07/31 16:54:41
# FileName : seg.py
################################

from MEHI.paralleled import preprocess as prep
from MEHI.paralleled import segmentation as seg
from MEHI.serial import IO
from MEHI.utils.tool import exeTime, log
from pyspark import SparkContext, SparkConf
import numpy as np
import time

conf = SparkConf().setAppName('seg').setMaster('local[64]').set('spark.executor.memory','20g').set('spark.driver.maxResultSize','20g').set('spark.driver.memory','40g').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2').set('spark.default.parallelism','256')

sc = SparkContext(conf=conf)
pwd = '/mnt/xfs_snode21/0401fusion'
s = time.time()

log('info')('load tiff ...')
sub_img = IO.load_tiff(pwd+'/sub_dev/')
fus_img = IO.load_tiff(pwd+'/fus_dev/')
log('info')('tiff load over ...')

rdd = sc.parallelize(sub_img)
rdd2 = sc.parallelize(fus_img)
p = rdd.zip(rdd2).collect()
print p.shape

sc.stop()
e = time.time()
log('time')("%.3f s in total." % (e-s))

