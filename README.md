# MEHI

Mouse Embryo Heart Imagery 
  
   ╯　　　 　╰   
  ●　　　 　 ●   
  " 　 　^　　"  
  
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
1) change the Input dir in the MEHI\_global.py or in the MEHI\_s\_global.py
```python
left_pwd = 'your image dir'
right_pwd = 'your image dir'
```
2) modify the MEHI\_main.py or the MEHI\_s\_main.py to customize your workflow
```python
L_img_stack, R_img_stack = init()
rddA, rddB = preprocess(L_img_stack, R_img_stack, 8)
rddB = registration(rddA, rddB, conf=0)
fuse_img = fusion(rddA, rddB)
segmentation(fuse_img)
```
3) start MEHI from terminal
```shell
python MEHI_s_main.py 
```

## More Information

### MEHI is broadly organized into:

- A main class with methods for initialization of Spark and control of the whole workflow.
- Classes for image processing module,like MEHI\_s\_fusion.
- Helper components like MEHI\_s\_IO, MEHI\_s\_common

### core API:

__Preprocessing__:  
- stripe\_removal(): 去横纹
- intensity\_normalization(): 亮度平衡，图像压缩
- sub\_background(): 减背景，去模糊  

__Registation&Fusion__:  
- mutual\_info(): 计算互信息
- q\_powell(): 计算对准向量
- get\_trans(): 实施对准变换
- q\_fusion(): 图像融合  

__Segmentation__:  
- Threshold(): otsu阈值粗分+watershed细分
- Properties(): 计算分割块的属性(坐标,朝向,大小...)
- Clustering(): 将2D分割按距离层次聚类
- Check(): 可视化分割结果  

## License
BSD
