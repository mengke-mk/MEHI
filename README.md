# MEHI

Mouse Embryo Heart Imagery 
  
[![Build Status](https://travis-ci.org/septicmk/MEHI.svg)](https://travis-ci.org/septicmk/MEHI)

## About

MEHI is a python library for processing large-scale 3D spatial and temporal mouse embryo date. the paralleled version is built on Spark.

MEHI includes the basic module for image processing, like preprocessing, registration, 2-side fusion, segmentation, tracking. the project contains two implementation, a paralleled version and a serial version. the paralleled version is written against Spark's Python API(Pyspark), making use of scipy, numpy, PuLP and pandas

## Requirements

 - Python 2.7
 - numpy 1.9+
 - pandas 0.16.1+
 - matplotlib 1.4+
 - PyWavelet 0.2.2+
 - scikit-image 0.11+
 - scipy 0.15+
 - pyspark 1.3.0
 - Cython 0.21+ 

## Quick Start

The paralleled version is designed to run on a cluster, but currently, I just test it on local mode. Anyway, you can get it work by following steps.  
1. first install the requirements by pip  
```shell
pip install -r requirements.txt
```
2. compile with cython  
```shell
make
```
you can use `make clean` to clean and `make test` to launch nosetest.  
3. install
```python
python setup.py install
```
or you can try `python setup.py develop` and `python setup.py develop --uninstall`  
then you can use `import MEHI`  

## More Information

### MEHI is broadly organized into:

- A main class with methods for initialization of Spark and control of the whole workflow.
- Classes for image processing module,like MEHI\_s\_fusion.
- Helper components like MEHI\_s\_IO, MEHI\_s\_common

### core API:

__Preprocessing__:  
- stripe\_removal(): 去横纹
- intensity\_normalization(): 亮度平衡，图像压缩
- saturation(): 饱和度调整   
- flip(): 翻转图像  
- invert(): 前景/背景转换  
- black\_tophat(): 黑帽滤波  
- subtract\_Background(): FIJI减背景  
- shrink(): 图像降维  
- projection(): 图像栈投影
- smooth(): 图像平滑  

__Registation&Fusion__:  
- mutual\_information(): 基于互信息的对准   
- cross\_correlation(): 基于互相关的对准  
- execute(): 实施对准向量  
- content\_fusion(): 基于局部熵的对准  
- wavelet\_fusion(): 基于小波变换的对准  

__Segmentation__:  
- Threshold(): otsu阈值粗分+watershed细分
- Properties(): 计算分割块的属性(坐标,朝向,大小...)
- Clustering(): 将2D分割按距离层次聚类

## License
BSD
