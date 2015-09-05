################################
# Author   : septicmk 
# Date     : 2015/07/30 15:30:35
# FileName : test_segmentation.py
################################

from MEHI.serial.segmentation import *
from MEHI.serial.IO import load_tiff
from test_utils import LocalTestCase
import numpy as np
from nose.tools import assert_equals
import os

L_pwd = os.path.abspath('.') + '/test_data/L_side_8/'
R_pwd = os.path.abspath('.') + '/test_data/R_side_8/'

class LocalTestSegmentationCase(LocalTestCase):
    def setUp(self):
        super(LocalTestSegmentationCase, self).setUp()
        self.L_imgs = load_tiff(L_pwd)
        self.R_imgs = load_tiff(R_pwd)

    def tearDown(self):
        super(LocalTestSegmentationCase, self).tearDown()

class TestSerialSegmentation(LocalTestSegmentationCase):

    def test_threshold(self):
        ret = threshold(self.L_imgs, 'adaptive', 15)
        assert (ret.shape == self.L_imgs.shape) 
        ret = threshold(self.L_imgs, 'otsu')
        assert (ret.shape == self.L_imgs.shape)
        ret = threshold(self.L_imgs, 'duel')
        assert (ret.shape == self.L_imgs.shape)

    def test_watershed_3d(self):
        binary = threshold(self.L_imgs, 'adaptive', 15)
        labeled_stack = watershed_3d(self.L_imgs, binary)
        assert (labeled_stack.shape == self.L_imgs.shape)
        #prop = properties(labeled_stack)
