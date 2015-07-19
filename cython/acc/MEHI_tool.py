################################
# Author   : septicmk
# Date     : 2015/4/3 9:13:31
# FileName : MEHI_tool.py
################################

import skimage.external.tifffile as tiff
import numpy as np
import os
from MEHI_common import *
from MEHI_global import *

class Img_IO:
    
    @exeTime
    def read(self, pwd):
        '''
        Usage:
         - just read all the image under the pwd
        '''
        img_stack = []
        names = []
        for imgname in os.listdir(pwd):
            if imgname.endswith('.tif'):
                names.append(imgname)
        names = sorted(names, key = lambda x: int(filter(str.isdigit, x)))
        #names = sorted(names, key = lambda x : int(x.partition('_')[2].partition('.')[0]))
        #print names
        z = 0
        for imgname in names:
            z += 1
            msg = "reading %d-th frame" % (z)
            end = len(names)
            bar('info')(msg, z, end)
            img_pwd = os.path.join(pwd, imgname)
            if img_pwd.endswith('.tif'):
                img = tiff.imread(img_pwd)
                img_stack.append(img)
        return np.array(img_stack)
    
    @exeTime
    def readone(self, pwd):
        '''
        Usage:
         - read the appointed img(img_stack)
        '''
        img_stack = tiff.imread(pwd)
        return img_stack 

    @exeTime 
    def write(self, name, img_stack):
        '''
        Usage:
         - write the img_stack
        '''
        tiff.imsave(name, img_stack) 
        
    @exeTime
    def write2f(self, name, img_stack):
        '''
        Usage:
         - write the img_stack in the form of individual tiff
        '''
        for z,frame in enumerate(img_stack):
            fname = output_pwd + name + '_%03d' % (z+1) + '.tif'
            #print fname
	    dir, file = os.path.split(fname)
	    if not os.path.exists(dir):
                os.makedirs(dir)
            tiff.imsave(fname, frame)
   
if __name__ == '__main__':
   IO = Img_IO()
   x = IO.readone('t.tif')
   IO.write2f('1-fusion',x)
   
    
