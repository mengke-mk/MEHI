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
log('info')('tiff load over ...')

rdd = sc.parallelize(sub_img)

log('info')('preprocess ...')
rdd = prep.saturation(rdd, 0.01)
rdd = prep.intensity_normalization(rdd)
#rdd = prep.smooth(rdd, 4)
log('info')('preprocess over ...')

log('info')('threshold start ...')
rdd = seg.threshold(rdd, 'phansalkar', 20)
rdd = seg.peak_filter(rdd, 140)
rdd = prep.smooth(rdd, 2)
binary = np.array(rdd.collect())
binary = (binary > 0).astype(np.uint8)

log('debug')('saving ...')
IO.save_tiff((binary).astype(np.uint8), pwd+'/bin_dev/phan_')


log('info')('load tiff ...')
fus_img = IO.load_tiff(pwd+'/fus_dev/')
log('info')('tiff load over ...')
rdd1 = sc.parallelize(fus_img)
rdd1 = prep.intensity_normalization(rdd1)
rdd1 = prep.subtract_Background(rdd1, 10)
rdd1 = seg.threshold(rdd1, 'otsu')
#rdd1 = prep.smooth(rdd1, 3)
memb = np.array(rdd1.collect())
memb = (memb > 0).astype(np.uint8)

log('debug')('saving ...')
IO.save_tiff((memb).astype(np.uint8), pwd+'/bin_m_dev/memb_')


def cut(binary, memb):
    img_zip = zip(binary, memb)
    def func(dframe):
        bf, mf = dframe[0].astype(np.intc), dframe[1].astype(np.intc)
        ans = (bf - mf) > 0
        ans = ans.astype(np.uint8)
        return ans
    return np.array(map(func, img_zip))

mn = cut(binary, memb)

log('debug')('saving ...')
IO.save_tiff((mn).astype(np.uint8), pwd+'/binary/mn_')

#tmp = zip(sub_img, binary)
#rdd = sc.parallelize(tmp)
#rdd = seg.watershed(rdd, 7)
#binary = np.array(rdd.collect())
#log('info')('threshold over ...')
#
#log('info')('fusion start ...')
#binary = IO.load_tiff(pwd+'/binary/')
#sub_img = IO.load_tiff(pwd+'/sub_dev/')
#prop = seg.fusion(binary, sub_img, 10, 30)
#prop = IO.load_table("_prop.pkl")
#prop.to_csv('_prop.csv')
#prop = seg.debug(binary,sub_img, 9, 70, prop)

sc.stop()
e = time.time()
log('time')("%.3f s in total." % (e-s))

