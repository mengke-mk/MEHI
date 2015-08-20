################################
# Author   : septicmk
# Date     : 2015/07/31 16:54:41
# FileName : seg.py
################################

from MEHI.paralleled import preprocess as prep
from MEHI.paralleled import segmentation as seg
from MEHI.paralleled import IO
from MEHI.utils.tool import exeTime, log
from pyspark import SparkContext, SparkConf
import numpy as np
import time

conf = SparkConf().setAppName('seg').setMaster('local[64]').set('spark.executor.memory','20g').set('spark.driver.maxResultSize','20g').set('spark.driver.memory','40g').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2').set('spark.default.parallelism','256')

sc = SparkContext(conf=conf)

pwd = '/mnt/xfs_snode21/CNN_data'
s = time.time()

log('info')('load tiff ...')
sub = IO.load_tiff(sc, pwd+'/train_n.tif')
log('info')('tiff load over ...')

rdd = sc.parallelize(sub)

#log('info')('subtract_Background ...')
#rdd = prep.subtract_Background(rdd, size=15)
#rdd = prep.invert(rdd)
#rdd = prep.subtract_Background(rdd, size=12)
#sub = np.array(rdd.collect())
#IO.save_tiff(sub, pwd+'/train_n.tif')

log('info')('preprocess ...')
#rdd = prep.saturation(rdd, 0.01)
rdd = prep.intensity_normalization(rdd, 8)
rdd = prep.smooth(rdd, 4)
log('info')('preprocess over ...')

log('info')('threshold start ...')
rdd = seg.threshold(rdd,'otsu')
binary = np.array(rdd.collect())
tmp = zip(sub, binary)
rdd = sc.parallelize(tmp)
rdd = seg.watershed(rdd, 6)
binary = np.array(rdd.collect())
log('info')('threshold over ...')

log('debug')('saving ...')
IO.save_tiff((binary).astype(np.uint8), pwd+'/ans.tif')

label = IO.load_tiff(sc, pwd+"/label.tif")
ans = IO.load_tiff(sc, pwd+"/ans.tif")
ans = np.where(ans>0,1,0)
label = np.where(label>0,1,0)
label = label.flatten()
ans = ans.flatten()
ans = label ^ ans
print ans.shape
t = (sum(ans)+.0)/ans.shape[0]
print "%.3f%%" % (t*100)
sc.stop()
e = time.time()
log('time')("%.3f s in total." % (e-s))

