.. _quickstart:

快速开始
========
要让项目运作起来，需要自己搭建一个合理的 `pipeline` 自己调取数据，预处理，对准融合，分割。你可以把它们写在一个脚本中使用 `python` 来执行。

流程
----
处理图像的流程根据实际调整，并没有一个特定的标准，不过还是有一个大致的框架。依次是读取图像，预处理，对准，融合，分割识别，然后分析。其中可能穿插这一些特定的图像变换，比如 `flip` `invert` 之类的操作。


存取图像
^^^^^^^^
首先是读取图像的 `IO.load_tiff()` ,通常有并行读取和串行读取两种方式，并行读取主要要传入参数 `sc` ,有时会发现串行读取反而比并行读取快，这是应为串行读取时会有cache，第一次读取之后之后相同的读取行为会快的多。另一方面，如果指定的读取数据后以 `.tif` 结尾则读取这一章，如果是以目录结尾则读取该目录下全部的 `tif` 并按名称排序，如果后面给上两个整数会读取指定的中间帧。

至于保存图像 `IO.save_tiff()` ，同样如果以 `.tif` 结尾则保存到一格文件中，以目录结尾则以单张的形式保存，如果不以字符 `/` 结尾则会把其用作前缀。保存图像的并串行版本都是同一个函数。

.. code-block:: python

    from MEHI.serial import _IO
    from MEHI.paralleled import IO
    from pyspark import SparkContext

    pwd = '/mnt/xfs_snode21/0401RawData/1-L-Red'
    sc = SparkContext()

    img_stack = _IO.load_tiff(pwd)
    img_stack = _IO.load_tiff(pwd, 250, 260)

    img_stack = IO.load_tiff(sc, pwd)
    img_stack = IO.load_tiff(sc, pwd, 250, 260)

    #保存的图像将存为 fus_0001 fus_002 ... 的形式
    IO.save_tiff(img_stack, '/mnt/xfs_snode21/0401TestData/fsuion/fus_')

预处理
^^^^^^
预处理也包含并行和串行的版本，区别是并行的参数对对象是 `RDD` 而串行的参数对象是一个 `ndarray` 。我相信大多数情况下你都会选择使用并行的模式。预处理基本上重点要做的有 **亮度平衡** **减背景** **翻转** 等。注意对 `Spark` 而言，其处理模式是 `Lazy` 的，也就是说大多数情况下你得用 `collect()` 来得到处理的结果。

.. code-block:: python

    from MEHI.paralleled import preprocess as prep
    from MEHI.serial import preprocess as _prep

    # 并行模式
    rdd = sc.parallelize(L_img_stack)
    rdd = prep.intensity_normalization(rdd)
    rdd = prep.flip(rdd)
    rdd = prep.subtract_Background(rdd)
    result = rdd.collect()

    # 串行模式
    img_stack = _prep.intensity_normalization(img_stack)
    img_stack = _prep.flip(img_stack)
    img_stack = _prep.subtract_Background(img_stack)

你会发现，并行和串行没什么不同的，只是传入的参数略有差别。

对准和融合
^^^^^^^^^^
对准和融合相当简单。大体上来讲，需要做的只有两步，第一步是互信息对准，第二步是小波变换融合。

.. code-block:: python

    from MEHI.paralleled import registration as reg
    from MEHI.paralleled import fusion as fus

    # imgA 和 imgB 分别是左右图像中对应的一对图像
    rddB = reg.mutual_information(rddB, imgA, imgB)
    rdd = rddA.zip(rddB)
    fused_img = fus.wavelet_fusion(rdd)

分割
^^^^
分割这一步比较混乱，因为尚没有摸索出一个较好的解决方案。所以我只能给出目前效果最好的方法。首先是阈值化，然后是2D分水岭，最后聚类成3D的。这一步耗时比较长。需要耐心调试。


.. DANGER:: 
    以下代码仅供参考。还请以实际调试为准。

.. code-block:: python

    from MEHI.paralleled import segmentation as seg
    from MEHI.paralleled import preprocess as prep
    
    # 首先需要减过背景的图像
    rdd = sc.parallelize(sub_img)
    rdd = seg.threshold(rdd, 'phansalkar', 20)
    rdd = seg.peak_filter(rdd, 140)
    rdd = rdd = prep.smooth(rdd, 2)
    
    # watershed
    rdd = sc.parallelize(sub_img).zip(rdd)
    rdd = seg.watershed(rdd, 7)
    binary = rdd.collect()
    
    # 聚类融合
    prop = seg.fusion(binary, sub_img, 10, 30)
    prop.to_csv("prop.csv")


脚本样例
--------

.. code-block:: python

    from MEHI.paralleled import IO
    from MEHI.paralleled import preprocess as prep
    from MEHI.paralleled import registration as reg
    from MEHI.paralleled import fusion as fus
    from MEHI.paralleled import segmentation as seg
    from MEHI.utils.tool import exeTime, log
    from pyspark import SparkContext, SparkConf
    import numpy as np
    import time

    conf = SparkConf().setAppName('seg').setMaster('local[64]').set('spark.executor.memory','20g').set('spark.driver.maxResultSize','20g').set('spark.driver.memory','40g').set('spark.local.dir','/dev/shm').set('spark.storage.memoryFraction','0.2').set('spark.default.parallelism','256')
    sc = SparkContext(conf=conf)
    pwd = '/mnt/xfs_snode21'

    log('info')('load tiff ...')
    L_img_stack = IO.load_tiff(sc, pwd+'/0401RawData/1-L-Red')
    rddA = sc.parallelize(L_img_stack)
    R_img_stack = IO.load_tiff(sc, pwd+'/0401RawData/1-R-Red')
    rddB = sc.parallelize(R_img_stack)

    log('info')('preprocess ...')
    _rddA = prep.intensity_normalization(rddA,8)
    _rddB = prep.intensity_normalization(rddB,8)
    _rddB = prep.flip(_rddB)
    rddB = prep.flip(rddB)
    L_img_stack_8 = np.array(_rddA.collect())
    R_img_stack_8 = np.array(_rddB.collect())
    imgA = L_img_stack_8[250]
    imgB = L_img_stack_8[250]

    log('info')('registration ...')
    rddB = reg.mutual_information(rddB)(imgA, imgB)

    log('info')('fusion ...')
    rdd = rddA.zip(rddB)
    fused_img = fus.wavelet_fusion(rdd)

    log('info')('preprocess ...')
    rdd = sc.parallelize(fused_img)
    rdd = prep.subtract_Background(rdd)
    rdd = prep.intensity_normalization(rdd)

    log('info')('segmentation ... ')
    rdd = seg.peak_filter(rdd, 140)
    rdd = prep.smooth(rdd, 2)
    rdd = sc.parallelize(sub_img).zip(rdd)
    rdd = seg.watershed(rdd, 7)
    binary = rdd.collect()
    prop = seg.fusion(binary, sub_img, 10, 30)
    prop.to_csv("prop.csv")

参数调整
--------
至于数据用几个 `partition` 采用几个进程，请根据实际情况酌情调整。不过还有一些重要的参数需要手动设置。::

    $ export SPARK_MEM=80g
    $ export TMPDIR=/home/mengke/MEHI_project/mytmp

除此之外，如果你认为spark的输出太过冗余，你可以去spark的配置文件存放目录下 `spark/conf/` 修改::

    log4j.rootCategory=ERROR, console

这样spark的输出就不会包含一些无用的 `INFO` 的信息

有关python中调用C的脚本参见 `blog <http://blog.septicmk.com/Python/use-Cython.html>`_ 


