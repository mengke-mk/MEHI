################################
# Author   : septicmk
# Date     : 2015/07/24 19:02:34
# FileName : test_registration.py
################################

from MEHI.serial.registration import *
from MEHI.serial.preprocess import flip
from MEHI.serial.IO import load_tiff
from test_utils import LocalTestCase
import numpy as np
from nose.tools import assert_equals
import os

L_pwd = os.path.abspath('.') + '/test_data/L_side_8/'
R_pwd = os.path.abspath('.') + '/test_data/R_side_8/'

class LocalTestRegistrationCase(LocalTestCase):
    def setUp(self):
        super(LocalTestRegistrationCase, self).setUp()
        self.L_imgs = load_tiff(L_pwd)
        self.R_imgs = load_tiff(R_pwd)
        self.imgA = self.L_imgs[0]
        self.imgB = flip(self.R_imgs)[0]
        self.vec0 = [0,0,0,1,1,0,0]

    def tearDown(self):
        super(LocalTestRegistrationCase, self).tearDown()

class TestSerialRegistration(LocalTestRegistrationCase):
    def test_p_powell(self):
        pass
        #vec = p_powell(self.imgA, self.imgB, self.vec0)
        #assert (abs(vec[0]-2) <= 5 and abs(vec[1]-3) <= 5 and abs(vec[2]-0) <= 0.5 and abs(vec[3]-1) <= 0.5 and abs(vec[4]-1) <= 0.5 and abs(vec[5]) < 0.2 and abs(vec[6]) < 0.2)
    
    def test_c_powell(self):
        vec = c_powell(self.imgA, self.imgB, self.vec0)
        assert (abs(vec[0]-2) <= 5 and abs(vec[1]-3) <= 5 and abs(vec[2]-0) <= 0.5 and abs(vec[3]-1) <= 0.5 and abs(vec[4]-1) <= 0.5 and abs(vec[5]) < 0.2 and abs(vec[6]) < 0.2)
    
    def test_execute(self):
        ret = execute(self.L_imgs, self.vec0) 
        assert_equals(sum(self.L_imgs.flatten()), sum(ret.flatten()))

    def test_mutual_information(self):
        ret = mutual_information(self.L_imgs, 0, self.vec0, self.imgA, self.imgB)
        assert (ret.shape == self.L_imgs.shape)
        assert (ret.dtype == self.L_imgs.dtype)

    def test_cross_correlation(self):
        img_stack = zip(self.L_imgs, self.R_imgs)
        ret = cross_correlation(img_stack)
        assert (ret.shape == self.L_imgs.shape)


