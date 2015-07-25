################################
# Author   : septicmk
# Date     : 2015/07/24 20:08:44
# FileName : test_p_fusion.py
################################

from MEHI.paralleled.fusion import *
from MEHI.paralleled.IO import load_tiff
from test_utils import PySparkTestCase
import numpy as np
import os

L_pwd = os.path.abspath('.') + '/test_data/L_side/'
R_pwd = os.path.abspath('.') + '/test_data/R_side/'

class PySparkTestFusionCase(PySparkTestCase):
    def setUp(self):
        super(PySparkTestFusionCase, self).setUp()
        self.L_imgs = load_tiff(self.sc, L_pwd)
        self.R_imgs = load_tiff(self.sc, R_pwd)
    
    def tearDown(self):
        super(PySparkTestFusionCase, self).tearDown()

class TestParalleledFusion(PySparkTestFusionCase):
    def test_content_fusion(self):
        img_stack = zip(self.L_imgs, self.R_imgs)
        rdd = self.sc.parallelize(img_stack)
        fused_img = content_fusion(rdd)
        assert (fused_img.dtype == self.L_imgs.dtype)
        assert (fused_img.shape == self.L_imgs.shape)
    
    def test_wavelet_fusion(self):
        img_stack = zip(self.L_imgs, self.R_imgs)
        rdd = self.sc.parallelize(img_stack)
        fused_img = wavelet_fusion(rdd)
        assert (fused_img.dtype == self.L_imgs.dtype)
        assert (fused_img.shape == self.L_imgs.shape)

