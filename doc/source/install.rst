.. _install:

安装
====
安装MEHI是极其简单的，但是首先你需要满足一下的一些依赖。

依赖
----

* python>=2.7.10 
* pip 
* gcc/g++
* Cython>=0.22.1
* matplotlib>=1.4.3
* nose>=1.3.7
* numpy>=1.9.2
* pandas>=0.16.1
* PyWavelets>=0.2.2
* scikit-image>=0.11.3
* scipy>=0.15.1

你可以在项目下找到 `requirement.txt` 这个文件。使用::

    $ pip install -r requirement.txt

可以使你快速安装这些依赖


环境配置
--------

主要是 `Spark` 的配置，下载 `Spark` 之后，你需要设置一下 `$SPARK_HOME` ::

    $ export SPARK_HOME=/home/mengke/MEHI_project/spark/spark-1.4.1-bin-hadoop1
    $ export PYTHONPATH=$SPARK_HOME/python/:$PYTHONPATH
    $ export PYTHONPATH=$SPARK_HOME/python/lib/py4j-0.8.2.1-src.zip:$PYTHONPATH
    $ export PATH=$SPARK_HOME/bin:$PAT

如果需要使用 `VTK` 的话，需要自己去使用 `cmake` 编译。编好之后，还需要添加如下的环境变量::

    $ export PYTHONPATH=$PYTHONPATH:/home/mengke/MEHI_project/VTK-build/bin:/home/mengke/MEHI_project/VTK-build/Wrapping/Python
    $ export PYTHONPATH=$PYTHONPATH:/home/mengke/MEHI_project/VTK-build/Wrapping/Python/vtk
    $ export LD_LIBRARY_PATH=/home/mengke/MEHI_project/VTK-build/lib:/home/mengke/MEHI_project/VTK-build/bin:/usr/local/lib
    $ export PYTHONPATH=$PYTHONPATH:$LD_LIBRARY_PATH

之后你可以测试一下

.. code-block:: python

    import VTK


编译
----
我还提供了一个简单的 `Makefile` 来管理整个工程。你可以用它来编译项目中使用C/C++编写的部分，你只需要输入::

    $ make

使用clean来清理::

    $ make clean

另外，我还使用nose编写了一些单元测试，可以供你检测环境是否部署正确。(需要先安装)::

    $ make test

这会需要一点时间来运行，如果全部通过则说明部署正确。

.. Attention:: 
    这只是表示运行不会报错，并不表示结果一定正确 

开发者模式
----------
我推荐的安装方式是使用开发者模式安装即::

    $ python setup.py install develop

这会使得你程序的改动直接被应用到项目上来，卸载则通过::

    $ python install develop --uninstall

这时你就可以在python中导入MEHI的包了

.. code-block:: python

    import MEHI
