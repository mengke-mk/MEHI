################################
# Author   : septicmk
# Date     : 2015/3/16 19:04:34
# FileName : MEHI_segmentation.py
################################

import skimage.io as io
io.use_plugin('tifffile')

from skimage.filters import threshold_otsu, threshold_adaptive, rank
from skimage.morphology import label
from skimage.measure import regionprops
from skimage.feature import peak_local_max
from skimage.morphology import disk, watershed
from scipy import ndimage
from scipy.spatial import distance as dist
import scipy.cluster.hierarchy as hier
import pandas as pd
import numpy as np
from itertools import groupby
from MEHI_s_common import *

class Segmentation:
    '''
    Usage:
     - segment all the image 
        1. read image as timepoint
        2. threshold_otsu in 2D
        3. label the regions
        4. cluster the segmentation across the z axis
        5. store data in the pandas.DataFrame
    '''
    def __init__(self):
        '''
        initialization
        '''
        self.smooth_size = 5
        self.min_radius = 9
        self.max_radius = 70

    @exeTime
    def threshold(self, image_stack):
        '''
        Usage:
         - threshold_otsu and watershed
        Args:
         - img_stack
         - rdd: rdd = sc.parallelize(img_stack)
        Return:
         - rdd: img stack after segmentation
        '''
        #z_size, x_size, y_size = image_stack.shape
        smooth_size = self.smooth_size
        #min_radius = self.min_radius 
        #max_int_proj = image_stack.max(axis=0)
        #threshold_global = threshold_otsu(max_int_proj)
        smoothed_stack = []
        ret_stack = []
        for z, frame in enumerate(image_stack):
            smoothed = rank.median(frame, disk(smooth_size)) 
            smoothed = rank.enhance_contrast(smoothed, disk(smooth_size))
            smoothed_stack.append(smoothed)
            #im_max = smoothed.max()
            #threshold = threshold_global
            #threshold = threshold_otsu(smoothed)
            #if im_max < threshold_global:
            #labeled = np.zeros(smoothed.shape, dtype=np.uint8)
            #else:
            #binary = smoothed > threshold
            binary = threshold_adaptive(smoothed, block_size=smooth_size)
            ret_stack.append(binary)
            #distance = ndimage.distance_transform_edt(binary)
            #local_maxi = peak_local_max(distance, min_distance=2*min_radius,
            #        indices=False, labels=smoothed)
            #markers = ndimage.label(local_maxi)[0]
            #labeled = watershed(-distance, markers, mask=binary)
        return np.array(smoothed_stack), np.array(ret_stack)

    @exeTime
    def watershed_3d(self, image_stack, binary):
        min_radius = self.min_radius
        distance = ndimage.distance_transform_edt(binary)
        local_maxi = peak_local_max(distance, min_distance=2*min_radius, indices=False, labels=image_stack)
        markers = ndimage.label(local_maxi)[0]
        labeled_stack = watershed(-distance, markers, mask=binary)
        return labeled_stack
    
    def labeln(self, properties, labeled_stack):
        '''
        Usage:
         - label the cell in 3d image with id
        Args:
         - properties: the properties of the image stack
         - labeled_stack: the labeled image stack
        Return:
         - cellmap: labeled 3d image 
        '''
        cellmap = labeled_stack.copy()
        index = properties.index.values
        z = properties['z'].copy().values
        tag = properties['tag'].copy().values
        trans = zip(index, z, tag)
        for key, group in groupby(trans, lambda x:x[1]):
            max_tag = reduce(lambda x,y: x[2] if (x[2] > y[2]) else y[2], list(group))
            tranf = np.zeros(max_tag+1)
            for u, _, v in group:
                tranf[v] = u
            cellmap[z] = tranf[cellmap[z]]
        return cellmap

    @exeTime
    def main(self, image_stack):  
        '''
        Usage:
         - return labeling img
        Args:
         - img_stack:
         - rdd: 
        Return: 
         - cell_table: info of each cell
        ''' 
        img_stack, ret_stack = self.threshold(image_stack)
        ret_stack = self.watershed_3d(image_stack, ret_stack)
        #labeled_stack = _rdd.collect()
        #properties = self.properties(labeled_stack, image_stack)
        #properties.to_pickle('properties.pkl')
        #properties = self.clustering(properties)
        #log('info')("clustering over")
        #cell_table = properties.groupby(level='label').apply(self.df_average, 'intensitysum')
        #cell_table.to_pickle("cell_table.pkl")
        #cell_table.to_csv("cell_show.csv")
        #cell_map = labeln(properties, labeled_stack)
        #del cell_table['tag']
        #return cell_map, cell_table
        return ret_stack

if __name__ == "__main__":
    ST = SegmentationTool()
    ST.main(0)
    #ST.debug()

