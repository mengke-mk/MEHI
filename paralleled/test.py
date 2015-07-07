import sys
sys.path.append('/home/mengke/spark/spark-1.2.1-bin-hadoop2.3/python')
sys.path.append('/home/mengke/spark/spark-1.2.1-bin-hadoop2.3/python/build')
from pyspark import SparkContext, SparkConf


class myTest:
    def add(self, rdd, tmp):
        def func(element):
            return element + tmp
        return rdd.map(func)


if __name__ == '__main__':
    conf = SparkConf().setAppName('test').setMaster('local[2]').set('spark.executor.memory','6g').set('spark.driver.maxResultSize','6g')
    sc = SparkContext(conf=conf)
    d = [1,2,3,4,5,6,7,8,9,10]
    distd = sc.parallelize(d)
    mt = myTest()
    p = mt.add(distd, 10).collect()
    sc.stop()
    print p
    
