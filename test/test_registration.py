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

L_pwd = os.path.abspath('.') + 'test_data/L_side/'
R_pwd = os.path.abspath('.') + 'test_data/R_side/'

class LocalTestRegistrationCase(LocalTestCase):
    def setUp(self):
        super(LocalTestRegistrationCase, self).setUp()
        self.L_imgs = load_tiff(L_pwd)
        self.R_imgs = load_tiff(R_pwd)
        self.imgA = L_imgs[0]
        self.imgB = flip(R_imgs)[0]
        self.vec0 = [0,0,0,1,1,0,0]

    def tearDown(self):
        super(LocalTestRegistrationCase, self).tearDown()

class TestSerialRegistration(LocalTestRegistrationCase):
    def test_p_powell():
        vec = p_powell(self.imgA, self.imgB, self.vec0)
        assert (abs(vec[0]-2) <= 5 and abs(vec[1]-13) <= 5 and abs(vec[2]-0) <= 0.5 and abs(vec[3]-1) <= 0.5 and abs(vec[4]-1) <= 0.5 and abs(vec[5]) < 0.2 and abs(vec[6]) < 0.2)
    
    def test_c_powell():
        vec = c_powell(self.imgA, self.imgB, self.vec0)
        assert (abs(vec[0]-2) <= 5 and abs(vec[1]-13) <= 5 and abs(vec[2]-0) <= 0.5 and abs(vec[3]-1) <= 0.5 and abs(vec[4]-1) <= 0.5 and abs(vec[5]) < 0.2 and abs(vec[6]) < 0.2)
    
    def test_execute():
        ret = execute(self.L_imgs, self.vec0) 
        assert_equals(self.L_imgs, ret)
