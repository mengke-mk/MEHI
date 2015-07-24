from cython.operator cimport dereference as deref
import cython
import numpy as np
cimport numpy as np


cdef extern from "sub_bg.h" namespace "prepocess":
    cdef cppclass Image:
        Image(int*, int, int) except +
        Image(int,int) except +
        int *data
        int H,W
        int getHeight()
        int getWidth()
        int getPixels()
        int getPixel(int, int)
        int putPixel(int, int, int)
        Image copy()
        void smooth()

    cdef cppclass RollingBall:
        RollingBall(int) except +
        unsigned char *data
        int patchwidth
        int shrinkfactor
        void buildRollingBall(int, int )

    cdef cppclass Rolling_Ball_Background:
        Image rollBall(RollingBall, Image, Image) 
        Image shrinkImage(Image, int) 
        int radius
        void interpolateBackground(Image, RollingBall)
        void extrapolateBackground(Image, RollingBall)
        Image subtractBackround(Image, int)
        void run(Image, int rd, int*)

@cython.boundscheck(False)
@cython.wraparound(False)

def subtract_Background(frame, radius):
    frame_int = frame.astype(np.intc)
    frame_f = frame_int.flatten()
    ret_f = np.zeros_like(frame_f)
    background = build_Background(frame_f, ret_f, radius)
    background = np.reshape(background, (2048, 2048))
    return (frame_int-background).clip(0,65535).astype(np.uint16)

def build_Background(np.ndarray[int, ndim=1, mode="c"] frame not None,
        np.ndarray[int, ndim=1, mode="c"] ret not None,
        int rd):
    cdef Rolling_Ball_Background *RBB = new Rolling_Ball_Background()
    cdef Image *cframe = new Image(&frame[0], 2048, 2048) 
    RBB.run(deref(cframe), rd, &ret[0])
    del RBB
    del cframe
    return ret
