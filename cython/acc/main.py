from MEHI_common import *
from MEHI_global import *
import MEHI_tool
import math
import trans

IO_tool = MEHI_tool.Img_IO()
r_img_stack = IO_tool.read(right_pwd)
vec=[-4.47617039e-01, 1.51950091e+01, 3.89617141e-03, 9.98441922e-01 , 9.94042566e-01, 2.24870341e-05, 3.14704115e-03]
frame = r_img_stack[100]

def get_trans(vec):
    tx, ty, sita, sx, sy, hx, hy = tuple(vec)
    A = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]])
    B = np.array([[math.cos(sita),  -math.sin(sita),  0], [math.sin(sita),  math.cos(sita),  0], [0, 0, 1]])
    C = np.array([[sx,  0,  0], [0, sy, 0], [0, 0, 1]])
    D = np.array([[1, hx, 0], [0, 1, 0], [0, 0, 1]])
    E = np.array([[1, 0, 0], [hy, 1 , 0], [0, 0, 1]])
    F = np.dot(np.dot(A,B),C)
    return np.dot(np.dot(F,D),E)

@exeTime
def func():
    U = get_trans(vec)
    ret = np.zeros_like(frame)
    trans.trans(frame, U, ret)
    return ret
ret = func()
IO_tool.write("acc.tif", ret)
