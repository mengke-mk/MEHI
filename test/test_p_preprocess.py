################################
# Author   : septicmk
# Date     : 2015/07/24 18:56:01
# FileName : test_p_preprocess.py
################################

from MEHI.paralleled.preprocess import *
from MEHI.paralleled.IO import load_tiff
from test_utils import PySparkTestCase
import numpy as np
import os

L_pwd = os.path.abspath('.') + '/test_data/L_side/'
R_pwd = os.path.abspath('.') + '/test_data/R_side/'

class PySparkTestPreprocessCase(PySparkTestCase):
    def setUp(self):
        super(PySparkTestPreprocessCase, self).setUp()
        self.L_imgs = load_tiff(self.sc, L_pwd)
        self.R_imgs = load_tiff(self.sc, R_pwd)
    
    def tearDown(self):
        super(PySparkTestPreprocessCase, self).tearDown()

class TestParalleledPreprocess(PySparkTestPreprocessCase):
    def test_stripe_removal(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = np.array(stripe_removal(rdd).collect())
        assert (ret.shape == self.L_imgs.shape) 
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_intensity_normalization(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = intensity_normalization(rdd).collect()
        ret = np.array(ret)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
        ret = intensity_normalization(rdd, 8).collect()
        ret = np.array(ret)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == np.uint8)
        ret = intensity_normalization(rdd, 16).collect()
        ret = np.array(ret)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == np.uint16)
    
    def test_flip(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = flip(rdd).collect()
        ret = np.array(ret)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_invert(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = invert(rdd).collect()
        ret = np.array(ret)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_black_tophat(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = black_tophat(rdd).collect()
        ret = np.array(ret)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_subtract_Background(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = subtract_Background(rdd).collect()
        ret = np.array(ret)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_shrink(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = shrink(rdd).collect()
        ret = np.array(ret)
        assert (ret.dtype == self.L_imgs.dtype)
        assert (ret.shape == (10, 256, 256))
    
    def test_projection(self):
        maxp = projection(self.L_imgs, 'max')
        minp = projection(self.L_imgs, 'min')
        meanp = projection(self.L_imgs, 'mean')
        assert (maxp.dtype == self.L_imgs.dtype and maxp.shape == self.L_imgs[0].shape)
        assert (minp.dtype == self.L_imgs.dtype and minp.shape == self.L_imgs[0].shape)
        assert (meanp.shape == self.L_imgs[0].shape)

    def test_smooth(self):
        rdd = self.sc.parallelize(self.L_imgs)
        ret = np.array(smooth(rdd, 10).collect())
        assert (ret.dtype == self.L_imgs.dtype)
        assert (ret.shape == self.L_imgs.shape)

