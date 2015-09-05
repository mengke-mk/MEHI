.. _segmentation:

细胞分割
========
并行和串行的相似，所以这里以并行版的为例，基本上把并行版中的 `rdd` 换成 `img_stack` 就能当串行版的使用。

分割的函数都还在不断修改中，所以使用起来很不方便。大体上就阈值化，分水岭，聚类，读取细胞信息用的比较多。

这包下面的函数跑出一些奇怪的结果是经常的事。

threshold(rdd, method='adaptive', *args)
----------------------------------------
阈值化，分割的关键所在，提供了四种阈值化方法。你也可以按需添加。

#. adaptive, 局部阈值法。需要传入一个参数 `block_size` 表示局部窗口的大小。
#. otsu, 全局阈值法，著名的otsu方法，用过的都说好。
#. duel, 我脑洞打开的产物，otsu的一个修改方法，并没有什么改进
#. phansalkar, 一种专门针对背景灰度变化大而设计的一种局部阈值法，目前效果最好，需要传入窗口大小。

强烈建议输入使用16位图像，8位图像输入会使某些方法的结果非常糟糕。

.. code-block:: python

    rdd = seg.threshold(rdd, method='adaptive', 14)
    rdd = seg.threshold(rdd, method='otsu')
    rdd = seg.threshold(rdd, method='duel')
    rdd = seg.threshold(rdd, method='phansalkar' 15)

peak_filter(rdd, smooth_size)
-----------------------------
用于去掉阈值化之后图像中的一些小碎块，目前的策略是移除低于一定像素面积的碎块，phansalkar阈值化后必须使用这个方法，不然结果很难看，输入只接受8位的阈值化后的图像。

.. code-block:: python

    rdd = seg.peak_filter(rdd, 70)

watershed(rdd, min_radius)
--------------------------
2D分水岭算法，只接受8位阈值化后的图像，min_radius表示最小的可接受的分块 **半径** 大小(我真希望这个值真的有效)。rdd是zip之后的图像。

.. code-block:: python

    rdd1 = sc.parallelize(binary) # 阈值化之后的图像
    rdd2 = sc.parallelize(sub_img_stack) # 减过背景的图像
    rdd = rdd2.zip(rdd1)
    rdd = seg.watershed(rdd, 6)

properties(labeled_stack, image_stack, min_radius, max_radius)
--------------------------------------------------------------
计算每个分出来的细胞的属性，比如重心，面积，亮度。这个函数在并行和串行的实现都是一样的，labeled_stack表示分水岭之后的图像，image_stack表示减背景的图像，min_radius和max_radius表示可接受的最小和最大的细胞半径

.. code-block:: python

    prop = seg.properties(labeled_stack, image_stack, 6, 70)

clustering(prop, threshold)
---------------------------
聚类，把2D的碎块聚类到3D上来。threshold表示聚类的停止距离

.. code-block:: python

    prop = seg.clustering(prop, 7)


fusion(labeled_stack, image_stack, min_radius, max_radius)
----------------------------------------------------------
上面两个函数的一个封装，参数列表同properties方法

.. code-block:: python

    cell_table = seg.fusion(labeled_stack, image_stack, 6, 70)



watershed_3d(image_stack, binary, min_distance=10, min_radius=6)
----------------------------------------------------------------
3D分水岭，极其极其极其极其耗时，不要轻易拿大数据尝试。

properties_3d(labeled_stack)
----------------------------
配套3D分水岭的一个计算分出来的细胞属性的方法。


