################################
# Author   : septicmk
# Date     : 2015/4/6 20:52:04
# FileName : MEHI_global.py
################################

import sys
sys.path.append('/home/mengke/spark/spark-1.3.0-bin-hadoop2.3/python')
sys.path.append('/home/mengke/spark/spark-1.3.0-bin-hadoop2.3/python/build')
from pyspark import SparkContext, SparkConf

#debug = True
debug = False

if debug:
    left_pwd = '/home/mengke/src/test/left'
    right_pwd = '/home/mengke/src/test/right'
    sample_index = 0
    wsize = 5
    bins = 256
    sgm1 = 41
    sgm2 = 88
    loglevel = ['debug','info','time','error','warn']
else:
    #left_pwd = '/mnt/share/Yao/RL_3d/20150401/E75/4/1-L-Red'
    #right_pwd = '/mnt/share/Yao/RL_3d/20150401/E75/4/1-R-Red'
    #left_pwd = '/mnt/MEHI_PEK/zwj/20150425/1-L-Green/L11'
    #right_pwd = '/mnt/MEHI_PEK/zwj/20150425/1-R-Green/L31'
    left_pwd = '/mnt/MEHI_PEK2/20150405sample/l1'
    right_pwd = '/mnt/MEHI_PEK2/20150405sample/r1'
    sample_index = 2#205
    wsize = 19
    bins = 256
    sgm1 = 41
    sgm2 = 88
    loglevel = ['debug','info','time','error','warn']
    #output_pwd = '/mnt/sdb_mnt/MEHI/fusion/1-Green/1'
    #output_pwd = '/mnt/MEHI_PEK2/20150405sample/parallel'
    output_pwd = '/mnt/xfs_snode21/MEHI_RAW_DATA/20150401/E75/4/2_result'
