################################
# Author   : septicmk
# Date     : 2015/09/05 16:58:28
# FileName : _intensity.pyx
################################

import numpy as np
cimport numpy as np
import cython

cpdef _saturation(int[:,:] frame, double precent):
    cdef int[:] H = np.zeros((256,), dtype = np.intc)
    cdef int[:,:] image = np.copy(frame)
    cdef double limit = precent*image.shape[0]*image.shape[1]
    cdef int b = -1,t = 256
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            H[image[i,j]] += 1
    cdef int fsum = 0
    cdef int rsum = 0
    for i in range(256):
        fsum += H[i]
        rsum += H[255-i]
        b = i if fsum <= limit else b
        t = 255-i if rsum <= limit else t
    return np.asarray(np.clip(image,b+1,t-1))

cpdef _saturation16(int[:,:] frame, double precent):
    cdef int[:] H = np.zeros((65536,), dtype = np.intc)
    cdef int[:,:] image = np.copy(frame)
    cdef double limit = precent*image.shape[0]*image.shape[1]
    cdef int b = -1,t = 65536
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            H[image[i,j]] += 1
    cdef int fsum = 0
    cdef int rsum = 0
    for i in range(65536):
        fsum += H[i]
        rsum += H[65535-i]
        b = i if fsum <= limit else b
        t = 65535-i if rsum <= limit else t
    return np.asarray(np.clip(image,b+1,t-1))


cpdef _normalization(int[:,:] frame, int conf):
    cdef int Max=-1,Min=65536
    cdef int[:,:] image = np.copy(frame)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            Max = max(Max, image[i,j])
            Min = min(Min, image[i,j])
    if Max == Min:
        Max = Min + 1
    cdef int muti = 255 if conf == 8 else 65535
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image[i,j] = (int) ( muti * (image[i,j] - Min) / (Max - Min) )
    return np.asarray(image)

def saturation(frame, precent):
    frame = np.array(frame)
    if frame.dtype == np.uint16:
        ret = _saturation16(frame.astype(np.intc), precent)
        return ret.astype(np.uint16)
    elif frame.dtype == np.uint8:
        ret = _saturation(frame.astype(np.intc), precent)
        return ret.astype(np.uint8)

def normalization(frame, dtype):
    frame = np.array(frame)
    if dtype == 16 or (not dtype and frame.dtype == np.uint16):
        ret = _normalization(frame.astype(np.intc), 16)
        return ret.astype(np.uint16)
    elif dtype == 8 or (not dtype and frame.dtype == np.uint8):
        ret = _normalization(frame.astype(np.intc), 8)
        return ret.astype(np.uint8)
