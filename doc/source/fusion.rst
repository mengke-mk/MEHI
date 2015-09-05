.. _fusion:

融合
====
并行和串行的相似，所以这里以并行版的为例，基本上把并行版中的 `rdd` 换成 `img_stack` 就能当串行版的使用。

融合只有两个函数，一个是基于局部熵的融合，一个是基于小波变换的融合。两种方法各有千秋，但是我倾向于使用小波变换融合。

content_fusion(rdd, sgm1=44, sgm2=81)
-------------------------------------
通过计算每个像素邻域的熵，并根据这个熵进行加权平均，不过论文对这个函数有一些优化，把它通过高斯卷积的方式实现了，所以 `sgm1` 和 `sgm2` 就变成两个神秘参数，定为44和81,最好不要去变，输入是一个zip过后的rdd，意义是把左右的图像一一对应的组合起来传入。可以接受8位和16位图像，输出为rdd。

.. code-block:: python

    rddA = sc.parallelize(L_img_stack)
    rddB = sc.parallelize(R_img_stack)
    rdd = rddA.zip(rddB)
    rdd = fus.content_fusion(rdd)

wavelet_fusion(rdd, level=5)
----------------------------
利用一个名为pywt的库实现的小波变换融合，这个pywt库底层是由C实现的，所以效率不用担心。 `level` 表示小波变换的层数，并不是越多越好，论文中的建议值是5, 你也可以根据实验的出更好的值。我定义的小波融合规则是低频取平均，高频取最大值，这个是比较流行的融合规则，有优点也有缺点。你也可以尝试别的融合规则。不过我都试过了，还是这个规则好。可以接受8位或16位，输出为rdd(使用的小波分解的类型也可以尝试修改，现在是使用论文推荐的 `db4` 小波)。

.. code-block:: python

    rddA = sc.parallelize(L_img_stack)
    rddB = sc.parallelize(R_img_stack)
    rdd = rddA.zip(rddB)
    rdd = fus.wavelet_fusion(rdd)

