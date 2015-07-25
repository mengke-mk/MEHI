################################
# Author   : septicmk
# Date     : 2015/07/24 15:38:36
# FileName : test_fusion.py
################################

from MEHI.serial.fusion import *
from MEHI.serial.IO import load_tiff
from test_utils import LocalTestCase
import numpy as np
import os,sys

L_pwd = os.path.abspath('.') + '/test_data/L_side/'
R_pwd = os.path.abspath('.') + '/test_data/R_side/'

class LocalTestFusionCase(LocalTestCase):
    def setUp(self):
        super(LocalTestFusionCase, self).setUp()
        self.L_imgs = load_tiff(L_pwd)
        self.R_imgs = load_tiff(R_pwd)

    def tearDown(self):
        super(LocalTestFusionCase, self).tearDown()

class TestSerailFusion(LocalTestFusionCase):

    def test_content_fusion(self):
        img_stack = zip(self.L_imgs, self.R_imgs)
        fused_img = content_fusion(img_stack)
        assert (fused_img.dtype == self.L_imgs.dtype)
        assert (fused_img.shape == self.L_imgs.shape)

    def test_wavelet_fusion(self):
        img_stack = zip(self.L_imgs, self.R_imgs)
        fused_img = wavelet_fusion(img_stack)
        assert (fused_img.dtype == self.L_imgs.dtype)
        assert (fused_img.shape == self.L_imgs.shape)
    
