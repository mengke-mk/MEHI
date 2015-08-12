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

conf = SparkConf().setAppName('seg').setMaster('local[128]').set('spark.executor.memory','20g').set('spark.driver.maxResultSize','20g').set('spark.driver.memory','40g').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2').set('spark.default.parallelism','512')
sc = SparkContext(conf=conf)

pwd = '/mnt/xfs_snode21'
s = time.time()

log('info')('load tiff ...')
fused_img = IO.load_tiff(sc, pwd+'/0401fusion/fus_dev')
log('info')('tiff load over ...')

rdd = sc.parallelize(fused_img)

log('info')('preprocess ...')
rdd = prep.invert(rdd)
rdd = prep.subtract_Background(rdd, size=11)
rdd = prep.saturation(rdd, 0.01)
rdd = prep.intensity_normalization(rdd, 8)
rdd = prep.smooth(rdd, 4)
log('info')('preprocess over ...')

log('info')('threshold start ...')
#rdd = seg.threshold(rdd,'otsu')
#rdd = seg.peak_filter(rdd, 4)
binary = np.array(rdd.collect())
log('info')('threshold over ...')

log('debug')('saving ...')
from skimage.morphology import remove_small_objects
#binary = remove_small_objects(binary, 12, connectivity=2)
IO.save_tiff((binary).astype(np.uint8), pwd+'/0401fusion/pie/pie')

#log('info')('watershed start ...')
#labeled_stack = seg.watershed_3d(fused_img, binary)
#log('info')('watershed over ...')

#log('info')('compute properties ...')
#prop = properties(labeled_stack)
#log('info')('saving ...')
#IO.save_table(prop,'seg_7_29.pkl')

sc.stop()
e = time.time()
log('time')("%.3f s in total." % (e-s))

