################################
# Author   : septicmk
# Date     : 2015/3/20 8:51:42
# FileName : MEHI_tracker.py
################################

import numpy as np
import pandas as pd
import itertools as it

class Tracker:
    def __init__(self):
        self.history = []
        
        
    def getF(self, i):
        if i == 0:
            a = np.array([[1,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,1,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,1,0,0],
                          [0,0,0,0,0,0,0,0,0]
                          [0,0,0,0,0,0,0,0,0]])
            return np.matrix(a)
        else if i == 1:
            a = np.array([[1,5,0,0,0,0,0,0,0],
                          [0,1,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,1,5,0,0,0,0],
                          [0,0,0,0,1,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0],
                          [0,0,0,0,0,0,1,5,0],
                          [0,0,0,0,0,0,0,1,0]
                          [0,0,0,0,0,0,0,0,0]])
            return np.matrix(a)
        else if i == 2:
            a = np.array([[1,5,12.5,0,0,0,0,0,0],
                          [0,1,5,0,0,0,0,0,0],
                          [0,0,1,0,0,0,0,0,0],
                          [0,0,0,1,5,12.5,0,0,0],
                          [0,0,0,0,1,5,0,0,0],
                          [0,0,0,0,0,1,0,0,0],
                          [0,0,0,0,0,0,1,5,12.5],
                          [0,0,0,0,0,0,0,1,5]
                          [0,0,0,0,0,0,0,0,1]])
            return np.matrix(a)
    
    def overlap(self, cmap1, cmap2, threshold):
        '''
        compute which cell in cmap1 overlap the cell in cmap2
        if the overlap rate is greater than threshold, then
        link them
        Args:
            cmap1: the volume of the lastframe
            cmap2: the volume of the currentframe
            threshold: the threshold of the overlap rate
        return:
            link: n*1 array indicata which cell overlap the i-th cell
        '''
        num = max(cmap2.flatten())
        link = np.zeros(num) 
        for i in range(num):
            mask = map(lambda x: 1 if x == i else 0, cmap2.flatten())
            vol = it.compress(cmap1.flatten(), mask)
            vol = np.array(list(vol)).astype(int)
            tmp = np.bincount(vol)
            ii = np.nonzero(tmp)[0]
            tmp = tmp/sum(tmp)
            overlap = zip(ii,tmp[ii])
            overlap = sorted(overlap,lambda x: x[1])
            if overlap[0][1] > threshold:
               link[i] = overlap[0][0]  
            else:
               link[i] = None
        
    def kalman(self, F, Sta, Cov, Z, H, R):
        #R = np.matrix(R)
        H = np.matrix(H)
        F = np.matrix(F)
        Z = np.matrix(Z)
        Sta = np.matrix(Sta)
        Cov = np.matrix(Cov)
        preSta = F * S
        preCov = F * Cov * F.T
        Kg = preCov * H.T * (H * preCov * H.T).I
        corSta = preSta + Kg * (Z - H*preSta)
        corCov = preCov - Kg * H * preCov
        return corSta, corCov
    
    def IMMf(self, P):
        pass
    

if __name__ == '__main__':
    tracker = Tracker()
        
        
