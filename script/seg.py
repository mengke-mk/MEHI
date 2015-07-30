################################
# Author   : septicmk
# Date     : 2015/07/29 20:37:37
# FileName : seg.py
################################

from MEHI.paralleled import preprocess as prep
from MEHI.paralleled import segmentation as seg
from MEHI.serial import IO
from MEHI.utils.tool import exeTime, log
from pyspark import SparkContext, SparkConf
import numpy as np
import time

conf = SparkConf().setAppName('test').setMaster('local[36]').set('spark.executor.memory','20g').set('spark.driver.maxResultSize','20g').set('spark.driver.memory','40g').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2').set('spark.default.parallelism','128')
sc = SparkContext(conf=conf)

pwd = '/mnt/md_5T/Galaxy_inst/pku_Galaxy/galaxy/database/ftp/liuyao@ncic.ac.cn'
s = time.time()

log('info')('load tiff ...')
fused_img = IO.load_tiff(pwd+'/0401fusion/fus_dev')
log('info')('tiff load over ...')

rdd = sc.parallelize(fused_img)

log('info')('preprocess ...')
rdd = prep.invert(rdd)
rdd = prep.subtract_Background(rdd, size=15)
rdd = prep.intensity_normalization(rdd,8)
rdd = prep.smooth(rdd, 6)
log('info')('preprocess over ...')

log('info')('threshold start ...')
rdd = seg.threshold(rdd,'duel')
#rdd = seg.peak_filter(rdd, 12)
binary = np.array(rdd.collect())
log('info')('threshold over ...')

log('debug')('saving ...')
from skimage.morphology import remove_small_objects
#binary = remove_small_objects(binary, 6, connectivity=3)
IO.save_tiff((255*binary).astype(np.uint8), pwd+'/0401fusion/binary/bin')

#log('info')('watershed start ...')
#labeled_stack = seg.watershed_3d(fused_img, binary)
#log('info')('watershed over ...')
#
#log('info')('compute properties ...')
#prop = properties(labeled_stack)
#log('info')('saving ...')
#IO.save_table(prop,'seg_7_29.pkl')

sc.stop()
e = time.time()
log('time')("%.3f s in total." % (e-s))

