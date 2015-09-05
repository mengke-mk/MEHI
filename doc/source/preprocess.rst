.. _preprocess:

预处理
======
并行和串行的相似，所以这里以并行版的为例，基本上把并行版中的 `rdd` 换成 `img_stack` 就能当串行版的使用。


stripe_removal(rdd)
-------------------
使用形态学的方法去除条纹，参数是内定的，会先做一次 `close` 在做一次 `open` , 16位和8位的数据都能接受。这个函数用的少，如果那天用到了，你就得去改源码了啊。输出是rdd，需要手动 `collect` 

intensity_normalization(rdd, dtype=None)
----------------------------------------
用于调节图像的亮度，同时也拿来改变图像的位数， `dtype` 参数如果不设置，就只是调节一下亮度。如果设置为8或者16,则表示输出按线性缩放为8位和16位的图像。内部调用的C的实现。输出是rdd，需要手动 `collect` 。

.. code-block:: python

    rdd = prep.intensity_normalization(rdd, 8)
    rdd = prep.intensity_normalization(rdd)


saturation(rdd, precent)
------------------------
用于调节图像的饱和度，就是把一定比例的最亮的点和最暗的点滤掉， `precent` 表示需要滤掉的比例，数值在0到1之间，推荐设置为 `0.01` ，不过请根据实际情况来。8位16位都可以，需要手动 `collect` 。

.. code-block:: python

    rdd = prep.saturation(rdd, 0.01)


flip(rdd)
---------
由于左右两边的图像是互为镜像的关系，所以需要对右边的图像进行翻转。直接用，输出为rdd， 需要手动 `collect` 


invert(rdd)
-----------
将图像的前景部分和背景部分的像素进行一次黑白交换，某些特殊函数的前置函数。8位和16位都可以，输出为rdd

black_tophat(rdd, size=15)
--------------------------
黑帽滤波，一种用于把圈状的细胞变成饼状细胞的手段，图像精度耗损很大但是运算速度很快。是基于skimage的库实现的。8位和16位的输入都可行，输出是rdd。


subtract_Background(rdd, size=12)
---------------------------------
原FIJI的减背景(FIJI用的java，这里改用的C++)，底层是C++的实现，单独使用可以用来去除背景的模糊，或者提取背景，和 `invert()` 使用，可以把圈状的细胞改变成饼状的细胞。16位和8位的输入都是可接受的。输出是rdd。size表示运算的窗口大小，依据实际情况调整。

.. code-block:: python

    rdd = prep.subtract_Background(rdd, 15)

shrink(rdd, shrink_size=2)
--------------------------
一个神奇的函数，用于对原图进行降维。比如把 `2048×2048` 的图像变成 `1024×2014` 的图像。 `shrink_size` 控制缩放的比例。比如 `shrink_size=2` 表示降维了一半，请务必保证这个值能被整除。可以接受8位或16位，输出是rdd。


projection(img_stack, method='max')
-----------------------------------
投影，把一个图像栈中z轴的图像投影到一张图上，可选的method有 `max` `min` `mean` 三个，分别表示投影时的策略。这个函数在并行和串行中都是一个函数，输入的 `img_stack` 是一个 `ndarray` 。8位和16位都可以输入。

.. code-block:: python

    rdd = prep.projection(rdd, method='mean')



smooth(rdd, smooth_size)
------------------------
用于对图像的边缘进行平滑，内部实现是一个中值滤波和一个对比度增强。注意，这个函数最好输入8位的图像，不建议输入16位的图像。 `smooth_size` 表示平滑时采用的圆形窗口的大小。一半设为个位数，数值越大，平滑的越厉害，有副作用，图像会比以前变得模糊，会把一些原本分开的图像连在一起，输出是rdd。

.. code-block:: python

    rdd = prep.smooth(rdd, 4)

blockshaped_all(img_stack, nrows, ncols)
----------------------------------------
一个神奇的函数，这个函数直接看源码可能不太容易明白，作用是把图像裁剪成一个个小块。这个函数的并行和串行版本都是同一个函数， `nrows` 和 `ncols` 表示裁剪出的每个小块的大小，比如你要把 `2048×2048` 的大图裁剪成许多个 `64×64` 的小块，那么 `nrows` 和 `ncols` 就设置为64。输入是 `ndarray` 。请务必保证 `nrows` 和 `ncols` 能够被整除。输出也是 `ndarray` 

.. code-block:: python

    arr_list = prep.blockshaped_all(img_stack, 64, 64)


recovershape_all(img_stack, nrows, ncols)
-----------------------------------------
上面那个函数的对应函数，用于把图像还原，用法和上面相同。 `nrows` 和 `ncols` 表示行和列要放置多少个小块才能还原。

.. code-block:: python

    img_stack = prep.blockshaped_all(arr_list, 32, 32)


