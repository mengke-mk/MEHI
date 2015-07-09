################################
# Author   : septicmk
# Date     : 2015/4/11 16:41:04
# FileName : MEHI_registration.py
################################

import numpy as np
import scipy.optimize as sciop
import math
from MEHI_s_global import *
from MEHI_s_common import *
import MEHI_s_preprocess
import MEHI_s_tool

class Registration:
    
    def init(self, imgA, imgB):
        self.imgA = imgA
        self.imgB = imgB
        self.H = self.generate_H(imgA, imgB)

    def generate_H(self, imgA, imgB):
        '''
        Usage:
         - calc the grey level histogram of imgA&B
        '''
        H = np.zeros((255,255))
        _X, _Y = imgA.shape
        for i in range(_X):
            for j in range(_Y):
                H[imgA[i,j],imgB[i,j]] += 1
        return H.astype(float)
   
    def mutual_info(self, H):
        '''
        Usage:
         - calc the -(mutual information)
        '''
        tot = .0+ sum(H.flatten())
        p = H/tot
        HAB = sum(map(lambda x: -x*math.log(x,2) if x>1e-7 else 0, p.flatten()))
        HA = sum(map(lambda x: -x*math.log(x,2) if x>1e-7 else 0, sum(p).flatten()))
        HB = sum(map(lambda x: -x*math.log(x,2) if x>1e-7 else 0, sum(p.T).flatten()))
        IAB = HA + HB - HAB
        return -IAB
    
    def PV_interpolation(self, H ,p, q):
        '''
        Usage:
         - update the grey level histogram
        '''
        imgA, imgB = self.imgA, self.imgB
        _X, _Y = imgA.shape
        px, py = p
        qx, qy = q
        dx, dy = qx-math.floor(qx), qy-math.floor(qy)
        if qx <= 0 or qx >= _X-1 or qy <= 0 or qy >= _Y-1:
            H[imgA[0,0],imgA[0,0]] += 1 
        else:
            H[imgA[int(math.floor(qx)),int(math.floor(qy))], imgB[px, py]] += (1-dx)*(1-dy)
            H[imgA[int(math.floor(qx)),int(math.ceil(qy))], imgB[px, py]] += dx*(1-dy)
            H[imgA[int(math.ceil(qx)),int(math.floor(qy))], imgB[px, py]] += (1-dx)*dy
            H[imgA[int(math.ceil(qx)),int(math.ceil(qy))], imgB[px, py]] += dx*dy
    
    def get_trans(self, vec):
        '''
        Usage:
         - calc the U from vec
        '''
        tx, ty, sita, sx, sy, hx, hy= tuple(vec)
        A = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
        B = np.array([[math.cos(sita),  -math.sin(sita),  0], [math.sin(sita),  math.cos(sita),  0], [0, 0, 1]])
        C = np.array([[sx,  0,  0], [0, sy, 0], [0, 0, 1]])
        D = np.array([[1, hx, 0], [0, 1, 0], [0, 0, 1]])
        E = np.array([[1, 0, 0], [hy, 1 , 0], [0, 0, 1]])
        F = np.dot(np.dot(A,B),C)
        return np.dot(np.dot(F,D),E)

    def update(self, vec):
        imgA, imgB, H = self.imgA, self.imgB, self.H
        _H = H.copy()
        _X, _Y = imgA.shape
        U = self.get_trans(vec)
        for i in range(_X):
            for j in range(_Y):
                p = np.array([i,j,1])
                q = np.dot(U, p)
                p = (p[0],p[1])
                q = (q[0],q[1])
                self.PV_interpolation(_H, p, q)
        return self.mutual_info(_H)
    
    @exeTime
    def match(self, img_stack_A, img_stack_B):
        '''
        Usage:
         - (discarded)
        '''
        n = len(img_stack_A)
        dft, x = float('inf'), 0
        for i in range(n):
            imgA, imgB = img_stack_A[i], img_stack_B[i]
            H = self.generate_H(imgA, imgB)
            tmp = self.mutual_info(H)
            #if 50 < i < n-50 and dft > tmp:
            if dft > tmp:
	        dft = tmp
                x = i
        log('info')('sample_index='+str(x))
        return x 
    
    def optimize(self, vec0, ej):
        '''
        Usage:
         - (discarded)
        '''
        vec = vec0.copy()
        s = self.update(vec)
        vec += ej
        c = self.update(vec)
        h = 1
        while abs(s-c) > 1e-3:
            if s > c:
                h = 2*h
            else:
                h = -h/4.0
            s, vec = c, vec + h*ej
            c = self.update(vec)
        return vec
    
    def powell(self, vec0):
        '''
        Usage:
         - (discarded)
        '''
        n = len(x0)
        e = []
        for j in range(n):
            tmp = [0]*n
            tmp[j] = 1
            e.append(tmp)
        e = np.array(e)
        vec = [vec0]
        dm = -float('inf')
        m = 0
        for j in range(n):
            vec.append(self.optimize(vec[j], e[j]))
            delta = self.update(vec[j]) - self.update(vec[j+1])
            if delta > dm:
                m, dm= j, delta
        ne = vec[n] - vec[0]
        if self.update(vec[0]) - 2*self.update(vec[n]) + self.update(2*vec[n] - vec[0]) < 2*dm:
            vectmp = self.optimize(vec[n] ,ne)
            vec.append(vectmp)
            
    @exeTime        
    def q_powell(self, imgA, imgB ,vec0):
        '''
        Usage:
         - calc the best vector
        '''
        self.init(imgA, imgB)
        def cb(xk):
            print xk
        ret = sciop.fmin_powell(self.update, vec0, callback=cb)
        return ret
    
    @exeTime
    def execute(self, rdd, vec):
        '''
        Usage:
         - Affine Transform the img stack using vec
        '''
        def func(frame):
            ret = []
            ret.append(self.trans(frame, vec))
            ret = np.array(ret)
            return ret
        return rdd.map(func)
              
    def trans(self, frame, vec):
        '''
        Usage:
         - for debug, it make no sense to you
        '''
        ret = np.zeros_like(frame)
        #ret = ret.astype(np.uint16)
        U = self.get_trans(vec)
        _X, _Y = frame.shape
        for x in range(_X):
            for y in range(_Y):
                tmp = np.array([x, y, 1])
                ans = np.dot(U, tmp)
                if (0 <= round(ans[0]) < _X) and (0 <= round(ans[1]) < _Y):
                    ret[round(ans[0]),round(ans[1])] = frame[x,y]
        return ret  

if __name__ == '__main__':
    IO_tool = MEHI_tool.Img_IO()
    prep = MEHI_preprocess.Preprocess()
    L_img_stack = IO_tool.read(left_pwd)
    R_img_stack = IO_tool.read(right_pwd)
    R_img_stack = prep.flip(R_img_stack)
    L_img_stack = prep.intensity_normalization(L_img_stack)
    R_img_stack = prep.intensity_normalization(R_img_stack)
    L_img_stack = prep.sub_background(L_img_stack)
    R_img_stack = prep.sub_background(R_img_stack)
    imgA = L_img_stack[0]
    imgB = R_img_stack[0]
    reg = Registration(imgA, imgB)
    vec0 = np.array([ -2, 14, 0, 1, 1])
    #imgB = reg.trans(imgB, vec0)
    #IO_tool.write('tl.tif', imgA)
    #IO_tool.write('tr.tif', imgB)
    ret = reg.q_powell(vec0)
    print ret
