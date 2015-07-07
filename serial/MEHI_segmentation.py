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
from MEHI_common import *
import matplotlib.pyplot as plt

class Segmentation:
    '''
    segment all the image 
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
        
    def read(self, time):
        '''
        read image according to time
        Args:
            time: current timepoint
        Returns:
            image_stack: tiff image list
        '''
        image_stack = io.imread('./embryo_8bit.tif')
        return image_stack
    
    @exeTime
    def threshold(self, image_stack, time):
        '''
        use threshold_otsu to compute the glaobal threshold, then
        binary the image, then
        label the image
        Args:
            image_stack: tiff image data
            time: current timepoint
        Returns:
            labeled_stack: labeled image 
        '''
        z_size, x_size, y_size = image_stack.shape
        smooth_size = self.smooth_size
        min_radius = self.min_radius 
        max_int_proj = image_stack.max(axis=0)
        threshold_global = threshold_otsu(max_int_proj)
        smoothed_stack = np.zeros_like(image_stack)
        labeled_stack = smoothed_stack.copy()
        
        end = len(image_stack)
        for z, frame in enumerate(image_stack):
            #print "processing the %i-th frame at %i-th timepoint " % (z,time)
            msg = "thresholding the %d-th" % (z+1)
            bar("info")(msg,z+1,end)
            #if z > 10: break
            smoothed = rank.median(frame, disk(smooth_size)) 
            smoothed = rank.enhance_contrast(smoothed, disk(smooth_size))
            smoothed_stack[z] = smoothed
            im_max = smoothed.max()
            threshold = threshold_global
            #threshold = threshold_otsu(smoothed)
            if im_max < threshold_global:
                labeled_stack[z] = np.zeros(smoothed.shape, dtype=np.int32)
            else:
                binary = smoothed > threshold
                #binary = threshold_adaptive(smoothed, block_size=smooth_size)
                distance = ndimage.distance_transform_edt(binary)
                local_maxi = peak_local_max(distance, min_distance=2*min_radius,
                        indices=False, labels=smoothed)
                markers = ndimage.label(local_maxi)[0]
                labeled_stack[z] = watershed(-distance, markers, mask=binary)
        return labeled_stack
    
    @exeTime
    def properties(self, labeled_stack, image_stack):
        '''
        get the properties of the segmentation, then
        store them into pandas.DataFrame
        Args:
            labeled_stack: labeled image
            image_stack: original image data
        Returns:
            properties: the properties list of segmentation 
        '''
        min_radius = self.min_radius
        max_radius = self.max_radius
        properties = []
        columns = ('x', 'y', 'z', 'intensitysum', 'size', 'tag')
        indices = []
        end = len(labeled_stack)
        for z, frame in enumerate(labeled_stack):
            msg = " get the properties of the %d-th" % (z+1)
            bar("info")(msg,z+1,end)
            f_prop = regionprops(frame.astype(np.int),
                    intensity_image = image_stack[z])
            for d in f_prop:
                radius = (d.area / np.pi)**0.5
                if(min_radius < radius < max_radius):
                    properties.append([d.weighted_centroid[0],
                                       d.weighted_centroid[1],
                                       z,d.mean_intensity*d.area,
                                       radius,
                                       d.label])
                    indices.append(d.label)
        if not len(indices):
            all_props = pd.DataFrame([], index=[])
        indices = pd.Index(indices, name='label')
        properties = pd.DataFrame(properties, index=indices, columns=columns)
        properties['intensitysum'] /= properties['intensitysum'].sum()
        return properties
    
    @exeTime
    def clustering(self, properties):
        '''
        hierarchical clustering
        Args:
            properties: the properties list of segmentation
        Returns:
            properties: labeled properties list 
        '''
        #print "clustering start..."
        log("info")("clustering start...")
        max_radius = self.max_radius
        positions = properties[['x', 'y', 'z']].copy()
        #dist_mat = dist.squareform(dist.pdist(positions.values))
        #link_mat = hier.linkage(dist_mat)
        #cluster_idx = hier.fcluster(link_mat, 6, criterion='distance')
        cluster_idx = hier.fclusterdata(positions.values, 6, criterion='distance')
        properties['new_label'] = cluster_idx
        properties.set_index('new_label', drop=True, append=False, inplace=True)
        properties.index.name = 'label' 
        properties = properties.sort_index()
        return properties
    
    def df_average(self, df, weights_column):
        values = df.copy().iloc[0]
        norm = df[weights_column].sum()
        for col in df.columns:
            try:
                v = (df[col] * df[weights_column]).sum() / norm
            except TypeError:
                v = df[col].iloc[0]
            values[col] = v
        return values
    
    def labeln(self, properties, labeled_stack):
        '''
        label the cell in 3d image with id
        Args:
            properties: the properties of the image stack
            labeled_stack: the labeled image stack
        Return:
            cellmap: labeled 3d image 
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
        return labeling img
        Args:
            time: current time
        Return: 
            cell_table: info of each cell
        ''' 
        labeled_stack = self.threshold(image_stack, time)
        properties = self.properties(labeled_stack, image_stack)
        properties.to_pickle('properties.pkl')
        properties = self.clustering(properties)
        log('info')("clustering over")
        cell_table = properties.groupby(level='label').apply(self.df_average, 'intensitysum')
        cell_table.to_pickle("cell_table.pkl")
        cell_table.to_csv("cell_show.csv")
        #cell_map = labeln(properties, labeled_stack)
        #del cell_table['tag']
        #return cell_map, cell_table
    
    @exeTime
    def debug(self):
        '''
        just for clustering debug
        '''
        prop = pd.read_pickle("properties.pkl")
        prop = self.clustering(prop)
        prop.to_csv("test.csv")
        cell_table = prop.groupby(level='label').apply(self.df_average, 'intensitysum')
        cell_table.to_pickle("cell_table.pkl")
   
   def check(self, frame):
   	labeled = threshold(frame)
	p = properties(labeled, frame)
	plane_props = p[p['z'] == 0]
	fig, axes = plt.subplots(1, 2, figsize=(16,32))
	axes[0].imshow(frame, interpolation='nearest', cmap='gray')
	axes[1].imshow(labeled, interpolation='nearest'. cmap='Dark2')
	axes[1].scatter(plane_props['y'], plane_props['x'], s=plane_props['intensitysum']*200, alpha=0.4)
	axes[1].scatter(plane_props['y'], plane_props['x'], s=40, marker='+', alpha=0.4)
        fig.hold(True)
	plt.hold(True)
	plt.show()



if __name__ == "__main__":
    ST = SegmentationTool()
    ST.main(0)
    #ST.debug()

