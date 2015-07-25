import cython
import numpy as np
cimport numpy as np
import math

cdef extern double c_update(unsigned char* imgA, unsigned char* imgB, double *U, int n)
@cython.boundscheck(False)
@cython.wraparound(False)

def get_trans(vec):
    tx, ty, sita, sx, sy, hx, hy= tuple(vec)
    A = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    B = np.array([[math.cos(sita),  -math.sin(sita),  0], [math.sin(sita),  math.cos(sita),  0], [0, 0, 1]])
    C = np.array([[sx,  0,  0], [0, sy, 0], [0, 0, 1]])
    D = np.array([[1, hx, 0], [0, 1, 0], [0, 0, 1]])
    E = np.array([[1, 0, 0], [hy, 1 , 0], [0, 0, 1]])
    F = np.dot(np.dot(A,B),C)
    return np.dot(np.dot(F,D),E)

def update(vec, np.ndarray[unsigned char, ndim=2, mode="c"] imgA not None,
                np.ndarray[unsigned char, ndim=2, mode="c"] imgB not None):
    cdef np.ndarray[double, ndim=2, mode="c"] U = get_trans(vec)
    return c_update(&imgA[0,0], &imgB[0,0], &U[0,0], imgA.shape[0])




