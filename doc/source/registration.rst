.. _registration:

对准
====
并行和串行的相似，所以这里以并行版的为例，基本上把并行版中的 `rdd` 换成 `img_stack` 就能当串行版的使用。

对准中只有一个重要函数，那就是 `mutual_information` 表示采用互信息进行对准。其他函数都很少用到。


p_powell(imgA, imgB ,vec0)
--------------------------
纯python实现的powell方法，效率感人，请勿随便使用，否则一跑就是一天，研究 `powell` 迭代方式使用，代码是写来看的。

c_powell(imgA, imgB ,vec0, ftol=0.01)
-------------------------------------
底层又C实现的powell方法，速度出奇的快，不过这个函数对用户是透明的，一般情况下用不到它，如果你要hack这个函数。imgA 和 imgB 表示用于对准的图像， 对准的参数有tx, `tx, ty, sita, sx, sy, hx, hy` 分别表示x的平移，y的平移，旋转弧度，s的缩放，y的缩放，x的剪切，y的剪切。 `vec0` 表示迭代开始的初始值。ftol表示最低可接受的精度，由于像素是离散的，所以这个精度太高到亚像素级也是没用的，0.1 0.01 就够了。

execute(rdd, vec)
-----------------
对一个图像栈进行一次仿射变换，vec表示仿射变换的参数，这个函数一般对用户透明，输出是rdd。

mutual_information(rdd, vec=None)
----------------------------------------
一般使用这个函数，如果vec是给定的值，则直接对图像进行指定的仿射变换，如果不指定vec的值，则需要传入对准用的图像 `imgA` 和 `imgB` 。这个函数经过curry化，当vec不为None时传入imgA或imgB，也可以人工控制迭代精度。

.. code-block:: python

    rdd = mutual_information(rdd)(imgA, imgB) # Curry化
    rdd = mutual_information(rdd)(imgA, imgB, 0.1) #控制精度
    rdd = mutual_information(rdd, [0,0,0,1,1,0,0])

cross_correlation(rdd)
----------------------
互相关对准，实验性质的实现，效果并不好，只能计算出一个x平移和y平移，不过速度很快。要实际使用这个函数内部还得修改。
