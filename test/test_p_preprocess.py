################################
# Author   : septicmk
# Date     : 2015/07/24 18:56:01
# FileName : test_p_preprocess.py
################################

from MEHI.parallized.preprocess import *
from MEHI.parallized.IO import load_tiff
from test_utils import PySparkTestCase
import numpy as np

L_pwd = os.path.abspath('.') + 'test_data/L_side/'
R_pwd = os.path.abspath('.') + 'test_data/R_side/'

class PySparkTestPreprocessCase(PySparkTestCase):
    def setUp():
        super(PySparkTestPreprocessCase, self).setUp()
        self.L_imgs = load_tiff(self.sc, L_pwd)
        self.R_imgs = load_tiff(self.sc, R_pwd)
    
    def tearDown():
        super(PySparkTestPreprocessCase, self).tearDown()

class TestParalleledPreprocess(PySparkTestPreprocessCase):
    def test_stripe_removal():
        rdd = sc.parallized(self.L_imgs)
        ret = stripe_removal(rdd).collect()
        assert (ret.shape == self.L_imgs.shape) 
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_intensity_normalization():
        rdd = sc.parallized(self.L_imgs)
        ret = intensity_normalization(rdd).collect()
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
        ret = intensity_normalization(rdd, 8)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == np.uint8)
        ret = intensity_normalization(rdd, 16) 
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == np.uint16)
    
    def test_flip():
        rdd = sc.parallized(self.L_imgs)
        ret = flip(rdd).collect()
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_invert():
        rdd = sc.parallized(self.L_imgs)
        ret = invert(rdd).collcet()
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_black_tophat():
        rdd = sc.parallized(self.L_imgs)
        ret = black_tophat(rdd).collect()
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_subtract_Background():
        rdd = sc.parallized(self.L_imgs)
        ret = subtract_Background(rdd).collect()
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)
    
    def test_shrink():
        rdd = sc.parallized(self.L_imgs)
        ret = shrink(rdd).collect()
        assert (ret.dtype == self.L_imgs.dtype)
        assert (ret.shape == (10, 256, 256))

