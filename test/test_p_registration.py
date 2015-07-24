################################
# Author   : septicmk
# Date     : 2015/07/24 18:56:05
# FileName : test_p_registration.py
################################

from MEHI.parallized.registration import *
from MEHI.serial.preprocess import flip
from MEHI.parallized.IO import load_tiff
from test_utils import PySparkTestCase
import numpy as np
from nose.tools import assert_equals

L_pwd = os.path.abspath('.') + 'test_data/L_side/'
R_pwd = os.path.abspath('.') + 'test_data/R_side/'

class PySparkTestRegistrationCase(PySparkTestCase):
    def setUp():
        super(PySparkTestRegistrationCase, self).setUp()
        self.L_imgs = load_tiff(self.sc, L_pwd)
        self.R_imgs = load_tiff(self.sc, R_pwd)
        self.imgA = L_imgs[0]
        self.imgB = flip(L_imgs)[0]
        self.vec0 = [0,0,0,1,1,0,0]
    
    def tearDown():
        super(PySparkTestRegistrationCase, self).tearDown()

class TestParalleledRegistration(PySparkTestRegistrationCase):
    def test_p_powell():
        vec = p_powell(self.imgA, self.imgB, self.vec0)
        assert (abs(vec[0]-2) <= 5 and abs(vec[1]-13) <= 5 and abs(vec[2]-0) <= 0.5 and abs(vec[3]-1) <= 0.5 and abs(vec[4]-1) <= 0.5 and abs(vec[5]) < 0.2 and abs(vec[6]) < 0.2)
    
    def test_c_powell():
        vec = c_powell(self.imgA, self.imgB, self.vec0)
        assert (abs(vec[0]-2) <= 5 and abs(vec[1]-13) <= 5 and abs(vec[2]-0) <= 0.5 and abs(vec[3]-1) <= 0.5 and abs(vec[4]-1) <= 0.5 and abs(vec[5]) < 0.2 and abs(vec[6]) < 0.2)
    
    def test_execute():
        ret = execute(self.L_imgs, self.vec0) 
        assert_equals(self.L_imgs, ret)
