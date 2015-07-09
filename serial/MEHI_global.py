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
    E75_fuse_pwd = '/mnt/xfs_snode21/MEHI_DECONVOLUTION/20150401/E75/4/1-0625-8bit/fusion'
    E75_L_pwd = '/mnt/xfs_snode21/MEHI_DECONVOLUTION/20150401/E75/4/1-L-Red'
    E75_R_pwd = '/mnt/xfs_snode21/MEHI_DECONVOLUTION/20150401/E75/4/1-R-Red'
    sample_index = 0
    wsize = 19
    bins = 256
    sgm1 = 41
    sgm2 = 88
    loglevel = ['debug','info','time','error','warn']
else:
    #left_pwd = '/mnt/Yao/20150401/E75/4/1-L-Red'
    #right_pwd = '/mnt/Yao/20150401/E75/4/1-R-Red'
    #left_pwd = '/mnt/MEHI_PEK2/20150405sample30/datal'
    #right_pwd = '/mnt/MEHI_PEK2/20150405sample30/datar'
    #left_pwd = '/mnt/xfs_snode21/MEHI_RAW_DATA/20150401/E75/4/2-L-Red'
    #right_pwd = '/mnt/xfs_snode21/MEHI_RAW_DATA/20150401/E75/4/2-R-Red'
    #left_pwd = '/mnt/xfs_snode21/MEHI_DECONVOLUTION/20150401/E75/4/1-L-Red'
    left_pwd = '/mnt/xfs_snode21/MEHI_DECONVOLUTION/20150401/E75/4/1-0625-8bit/fusion'
    right_pwd = '/mnt/xfs_snode21/MEHI_DECONVOLUTION/20150401/E75/4/1-R-Red'
    #left_pwd = '/mnt/xfs_snode21/MEHI_Test_data/20150401sample/1-L-Red'
    #right_pwd = '/mnt/xfs_snode21/MEHI_Test_data/20150401sample/1-R-Red'
    sample_index = 105
    wsize = 19
    bins = 256
    sgm1 = 41
    sgm2 = 88
    loglevel = ['debug','info','time','error','warn']
    #output_pwd = '/mnt/xfs_snode21/MEHI_RAW_DATA/20150401/E75/4/2_result'
    output_pwd = '/mnt/xfs_snode21/MEHI_PROCESS_DATA/20150401/E75/4/1-Result-0628serialtime'
    #output_pwd = '/mnt/xfs_snode21/MEHI_Test_data/20150401sample/1-result-0625'
