.. MEHI documentation master file, created by
   sphinx-quickstart on Thu Sep  3 19:43:13 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MEHI 使用指南
=============

MEHI是一个基于python的具有处理大规模3D时空数据能力(笑)的生物图像处理系统，其并行机制基于 `Spark1.4.1 <http://spark.apache.org/>`_ ,其主要的研究对象是小鼠胚胎的心脏成像数据。

MEHI包含图像处理的基本模块，比如预处理，对准，融合，分割，(追踪)，可视化。整个项目包含两个实现，一个并行版本，一个串行版本，其主要的算法支持来源于Scipy，Scikit-Image，Numpy，pandas。并采用以python搭建框架，然后C/C++来处理计算的方式，与pySpark实现的64进程并行加速，极大缩短了运行时间。

这个简单的文档将告诉你如何使用MEHI这个库，API使用的注意事项，以及一些基本的例子。如果你赶时间，可以直接阅读第二章。另外，如果你在运行时发生的bug，请尽量从文档中获取支持，尤其是最后一章，列出了一些可能遇见的报错问题。顺便一说，这个文档只是一个参考，毕竟写的很仓促，一些错误是难免的。如果文档中的例子，描述和实际情况有出入，你TM来打我啊?

目录:

.. toctree::
   :numbered:
   :maxdepth: 2

   install
   quickstart
   preprocess
   registration
   fusion
   segmentation
   utils
   issues


Indices and tables
==================

* :ref:`search`

