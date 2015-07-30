################################
# Author   : septicmk
# Date     : 2015/07/30 15:15:42
# FileName : test_p_segmentation.py
################################

from MEHI.paralleled.segmentation import *
from MEHI.paralleled.IO import load_tiff
from test_utils import PySparkTestCase
import numpy as np
from nose.tools import assert_equals
import os

L_pwd = os.path.abspath('.') + '/test_data/L_side_8/'
R_pwd = os.path.abspath('.') + '/test_data/R_side_8/'

class PySparkTestSegmentationCase(PySparkTestCase):
    def setUp(self):
        super(PySparkTestSegmentationCase, self).setUp()
        self.L_imgs = load_tiff(self.sc, L_pwd)
        self.R_imgs = load_tiff(self.sc, R_pwd)
    
    def tearDown(self):
        super(PySparkTestSegmentationCase, self).tearDown()

class TestParalleledSegmentation(PySparkTestSegmentationCase):

    def test_threshold(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = np.array(threshold(rdd, 'adaptive', 15).collect())
        assert (ret.shape == self.L_imgs.shape) 
        ret = np.array(threshold(rdd, 'otsu').collect())
        assert (ret.shape == self.L_imgs.shape)
        ret = np.array(threshold(rdd, 'duel').collect())
        assert (ret.shape == self.L_imgs.shape)

    def test_watershed_3d(self):
        rdd = self.sc.parallelize(self.L_imgs)
        binary = threshold(rdd, 'adaptive', 15).collect()
        binary = np.array(binary)
        labeled_stack = watershed_3d(self.L_imgs, binary)
        assert (labeled_stack.shape == self.L_imgs.shape)
        prop = properties(labeled_stack)
