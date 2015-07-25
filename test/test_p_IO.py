################################
# Author   : septicmk
# Date     : 2015/07/24 18:47:22
# FileName : test_p_IO.py
################################

from MEHI.paralleled.IO import *
from test_utils import PySparkTestCase
import os
import numpy as np

L_pwd = os.path.abspath('.') + '/test_data/L_side/'
R_pwd = os.path.abspath('.') + '/test_data/R_side/'

class TestParalleledIO(PySparkTestCase):
    def test_load_tiff(self):
        img_stack = load_tiff(self.sc, L_pwd, 2,7)
        assert (img_stack.shape == (5,512,512))
        assert (img_stack.dtype == np.uint16)

