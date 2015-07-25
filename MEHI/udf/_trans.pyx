import cython
import numpy as np
cimport numpy as np

cdef extern void c_trans8(unsigned char* frame, double *U, unsigned char *ret, int m)
cdef extern void c_trans16(unsigned short* frame, double *U, unsigned short* ret, int m)
@cython.boundscheck(False)
@cython.wraparound(False)

def trans8(np.ndarray[unsigned char, ndim=2, mode="c"] frame not None,
          np.ndarray[double, ndim=2, mode="c"] U not None,
          np.ndarray[unsigned char, ndim=2, mode="c"] ret not None):
    c_trans8(&frame[0,0], &U[0,0], &ret[0,0], frame.shape[0])
    return ret 

def trans16(np.ndarray[unsigned short, ndim=2, mode="c"] frame not None,
          np.ndarray[double, ndim=2, mode="c"] U not None,
          np.ndarray[unsigned short, ndim=2, mode="c"] ret not None):
    c_trans16(&frame[0,0], &U[0,0], &ret[0,0], frame.shape[0])
    return ret 

def trans(frame, U, ret):
    if frame.dtype == np.uint8:
        trans8(frame, U, ret)
    elif frame.dtype == np.uint16:
        trans16(frame, U, ret)
