################################
# Author   : septicmk
# Date     : 2015/09/05 16:56:03
# FileName : _phansalkar.pyx
################################

import cython
import numpy as np
cimport numpy as np

cdef extern void c_phansalkar(double* frame, int wsize, int size, unsigned char* ret)

@cython.boundscheck(False)
@cython.wraparound(False)
cdef _phansalkar(double[:,:] frame, int wsize, int size, unsigned char[:,:]ret):
    c_phansalkar(&frame[0,0], wsize, size, &ret[0,0])

def phansalkar(frame, wsize):
    frame = frame.astype(np.float64)
    ret = np.ones_like(frame, dtype=np.uint8)
    _phansalkar(frame, wsize, frame.shape[0], ret)
    return ret



