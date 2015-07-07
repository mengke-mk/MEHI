################################
# Author   : septicmk
# Date     : 2015/4/6 20:52:04
# FileName : MEHI_global.py
################################

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
    left_pwd = '/mnt/Yao/20150401/E75/4/1-L-Red'
    right_pwd = '/mnt/Yao/20150401/E75/4/1-R-Red'
    sample_index = 200
    wsize = 19
    bins = 256
    sgm1 = 41
    sgm2 = 88
    loglevel = ['debug','info','time','error','warn']
