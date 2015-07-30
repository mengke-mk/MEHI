from cython.operator cimport dereference as deref
import cython
import numpy as np
cimport numpy as np


cdef extern from "_subtract_bg_c.h" namespace "prepocess":
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

    cdef cppclass Rolling_Ball_Background_8:
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
    _X,_Y = frame.shape
    if frame.dtype == np.uint16:
        frame_int = frame.astype(np.intc)
        frame_f = frame_int.flatten()
        ret_f = np.zeros_like(frame_f)
        background = build_Background(frame_f, ret_f, radius, _X)
        background = np.reshape(background, (_X, _Y))
        return (frame_int-background).clip(0,65535).astype(np.uint16)
        #return background.clip(0,65535).astype(np.uint16)
    elif frame.dtype == np.uint8:
        frame_int = frame.astype(np.intc)
        frame_f = frame_int.flatten()
        ret_f = np.zeros_like(frame_f)
        background = build_Background_8(frame_f, ret_f, radius, _X)
        background = np.reshape(background, (_X, _Y))
        return (frame_int-background).clip(0,255).astype(np.uint8)
    else:
        return frame


def build_Background(np.ndarray[int, ndim=1, mode="c"] frame not None,
        np.ndarray[int, ndim=1, mode="c"] ret not None,
        int rd, int n):
    cdef Rolling_Ball_Background *RBB = new Rolling_Ball_Background()
    cdef Image *cframe = new Image(&frame[0], n, n) 
    RBB.run(deref(cframe), rd, &ret[0])
    del RBB
    del cframe
    return ret

def build_Background_8(np.ndarray[int, ndim=1, mode="c"] frame not None,
        np.ndarray[int, ndim=1, mode="c"] ret not None,
        int rd, int n):
    cdef Rolling_Ball_Background_8 *RBB = new Rolling_Ball_Background_8()
    cdef Image *cframe = new Image(&frame[0], n, n) 
    RBB.run(deref(cframe), rd, &ret[0])
    del RBB
    del cframe
    return ret


