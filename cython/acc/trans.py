import numpy as np
import math

def get_trans(vec):
    tx, ty, sita, sx, sy, hx, hy = tuple(vec)
    A = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    B = np.array([[math.cos(sita),  -math.sin(sita),  0], [math.sin(sita),  math.cos(sita),  0], [0, 0, 1]])
    C = np.array([[sx,  0,  0], [0, sy, 0], [0, 0, 1]])
    D = np.array([[1, hx, 0], [0, 1, 0], [0, 0, 1]])
    E = np.array([[1, 0, 0], [hy, 1 , 0], [0, 0, 1]])
    F = np.dot(np.dot(A,B),C)
    return np.dot(np.dot(F,D),E)

def trans(frame, vec):
    ret = np.zeros_like(frame)
    U = get_trans(vec)
    _X, _Y = frame.shape
    for x in range(_X):
        for y in range(_Y):
            tmp = np.array([x, y, 1])
            ans = np.dot(U, tmp)
            if (0 <= round(ans[0]) < _X) and (0 <= round(ans[1]) < _Y):
                ret[round(ans[0]),round(ans[1])] = frame[x,y]
    return ret 
