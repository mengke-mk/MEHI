################################
# Author   : septicmk
# Date     : 2015/07/24 19:41:26
# FileName : test_utils.py
################################

import shutil
import tempfile
import unittest
from numpy import vstack
from pyspark import SparkContext


class PySparkTestCase(unittest.TestCase):
    def setUp(self):
        class_name = self.__class__.__name__
        self.sc = SparkContext('local', class_name)
        self.sc._jvm.System.setProperty("spark.ui.showConsoleProgress", "false")
        log4j = self.sc._jvm.org.apache.log4j
        log4j.LogManager.getRootLogger().setLevel(log4j.Level.FATAL)

    def tearDown(self):
        self.sc.stop()
        # To avoid Akka rebinding to the same port, since it doesn't unbind
        # immediately on shutdown
        self.sc._jvm.System.clearProperty("spark.driver.port")


class PySparkTestCaseWithOutputDir(PySparkTestCase):
    def setUp(self):
        super(PySparkTestCaseWithOutputDir, self).setUp()
        self.outputdir = tempfile.mkdtemp()

    def tearDown(self):
        super(PySparkTestCaseWithOutputDir, self).tearDown()
        shutil.rmtree(self.outputdir)


class LocalTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

class LocalTestCaseWithOutputDir(LocalTestCase):

    def setUp(self):
        super(LocalTestCaseWithOutputDir, self).setUp()
        self.outputdir = tempfile.mktemp()

    def tearDown(self):
        super(LocalTestCaseWithOutputDir, self).tearDown()
        shutil.rmtree(self.outputdir)
