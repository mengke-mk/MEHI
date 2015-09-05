################################
# Author   : septicmk
# Date     : 2015/09/05 16:58:36
# FileName : _moment.pyx
################################

import numpy as np
cimport numpy as np
import cython

cpdef _moment(double[:,:,:] image):
    cdef double[:] mu = np.zeros((4,),dtype = np.double)
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            for z in range(image.shape[2]):
                if image[x,y,z] > 0:
                    mu[0] += 1
                    mu[1] += x
                    mu[2] += y
                    mu[3] += z
    mu[1] = mu[1]/mu[0]
    mu[2] = mu[2]/mu[0]
    mu[3] = mu[3]/mu[0]
    return np.asarray(mu)

def moment(image):
    return _moment(image.astype(np.double))

