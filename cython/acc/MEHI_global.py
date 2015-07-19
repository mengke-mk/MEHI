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
    #left_pwd = '/mnt/share/Yao/RL_3d/20150401/E75/4/1-L-Red'
    #right_pwd = '/mnt/share/Yao/RL_3d/20150401/E75/4/1-R-Red'
    #left_pwd = '/mnt/MEHI_PEK/zwj/20150425/1-L-Green/L11'
    #right_pwd = '/mnt/MEHI_PEK/zwj/20150425/1-R-Green/L31'
    left_pwd = '/mnt/md_5T/Galaxy_inst/pku_Galaxy/galaxy/database/ftp/liuyao@ncic.ac.cn/0401RawData/1-L-Red'
    right_pwd = '/mnt/md_5T/Galaxy_inst/pku_Galaxy/galaxy/database/ftp/liuyao@ncic.ac.cn/0401RawData/1-R-Red'
    #left_pwd = '/mnt/MEHI_PEK2/20150405sample30/datal'
    #right_pwd = '/mnt/MEHI_PEK2/20150405sample30/datar'
    sample_index = 2
    wsize = 19
    bins = 256
    sgm1 = 41
    sgm2 = 88
    loglevel = ['debug','info','time','error','warn']
    #output_pwd = '/mnt/sdb_mnt/MEHI/fusion/1-Green/1'
    output_pwd = '/mnt/md_5T/Galaxy_inst/pku_Galaxy/galaxy/database/ftp/liuyao@ncic.ac.cn/0401fusion'

