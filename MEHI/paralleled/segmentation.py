################################
# Author   : septicmk
# Date     : 2015/08/16 16:17:14
# FileName : segmentation.py
################################

from MEHI.utils.tool import exeTime, bar, log
import numpy as np


def threshold(rdd, method='adaptive', *args):
    from skimage.filters import threshold_otsu, threshold_adaptive
    import scipy.ndimage as ndi
    def adaptive(frame):
        binary = threshold_adaptive(frame, block_size=block_size)
        #binary = ndi.binary_fill_holes(binary)
        return binary
    def otsu(frame):
        threshold = threshold_otsu(frame)
        binary = frame > threshold
        return binary
    def duel(frame):
        threshold = threshold_otsu(frame)
        binary1 = frame > threshold
        frame = frame - binary1 * frame
        threshold = threshold_otsu(frame)
        binary2 = frame > threshold
        binary = binary2
        return binary
    if method=='adaptive':
        block_size = args[0]
        return rdd.map(adaptive)
    elif method == 'otsu':
        return rdd.map(otsu)
    elif method == 'duel':
        return rdd.map(duel)
    else:
        raise "Bad Threshold Method", method

def peak_filter(rdd, smooth_size):
    from skimage.morphology import disk, binary_opening
    def func(frame):
        opened = binary_opening(frame, disk(smooth_size))
        opened = opened & frame
        return opened
    return rdd.map(func)


def watershed(rdd, min_radius):
    from skimage.morphology import watershed, remove_small_objects
    from scipy import ndimage
    from skimage.feature import peak_local_max
    def func(dframe):
        frame, binary = dframe[0], dframe[1]
        #binary = remove_small_objects(binary, min_radius, connectivity=2)
        distance = ndimage.distance_transform_edt(binary)
        local_maxi = peak_local_max(distance, min_distance=2*min_radius, indices=False, labels=frame)
        markers = ndimage.label(local_maxi)[0]
        labeled = watershed(-distance, markers, mask=binary)
        return labeled
    return rdd.map(func)

@exeTime
def properties(labeled_stack, image_stack, min_radius, max_radius):
    import pandas as pd
    from skimage.measure import regionprops
    prop = []
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
                prop.append([d.weighted_centroid[0],
                                   d.weighted_centroid[1],
                                   z,d.mean_intensity*d.area,
                                   radius,
                                   d.label])
                indices.append(d.label)
    if not len(indices):
            all_props = pd.DataFrame([], index=[])
    indices = pd.Index(indices, name='label')
    prop = pd.DataFrame(prop, index=indices, columns=columns)
    prop['intensitysum'] /= prop['intensitysum'].sum()
    return prop


@exeTime
def clustering(prop, threshold):
    import scipy.cluster.hierarchy as hier
    log("info")("clustering start...")
    positions = prop[['x', 'y', 'z']].copy()
    print positions.values.shape
    log("info")("akka")
    cluster_idx = hier.fclusterdata(positions.values, threshold, criterion='distance')
    log("info")("ooover")
    prop['new_label'] = cluster_idx
    prop.set_index('new_label', drop=True, append=False, inplace=True)
    prop.index.name = 'label' 
    prop = prop.sort_index()
    return prop

def df_average(df, weights_column):
    values = df.copy().iloc[0]
    norm = df[weights_column].sum()
    for col in df.columns:
        try:
            v = (df[col] * df[weights_column]).sum() / norm
        except TypeError:
            v = df[col].iloc[0]
        values[col] = v
    return values

@exeTime
def fusion(labeled_stack, image_stack, min_radius, max_radius):  
    prop = properties(labeled_stack, image_stack, min_radius, max_radius)
    prop.to_pickle('prop.pkl')
    prop = clustering(prop, 10)
    log('info')("clustering over")
    cell_table = prop.groupby(level='label').apply(df_average, 'intensitysum')
    cell_table.to_pickle("cell_table.pkl")
    cell_table.to_csv("cell_show.csv")
    #cell_map = labeln(properties, labeled_stack)
    del cell_table['tag']
    return cell_table

def debug(labeled_stack, image_stack, min_radius, max_radiusm, prop):
    prop = clustering(prop,6)
    log('info')("clustering over")
    cell_table = prop.groupby(level='label').apply(df_average, 'intensitysum')
    cell_table.to_pickle("cell_table.pkl")
    cell_table.to_csv("cell_show.csv")
    #cell_map = labeln(properties, labeled_stack)
    del cell_table['tag']
    return cell_table



@exeTime
def watershed_3d(image_stack, binary, min_distance=10, min_radius=6):
    from skimage.morphology import watershed, remove_small_objects
    from scipy import ndimage
    from skimage.feature import peak_local_max
    binary = remove_small_objects(binary, min_radius, connectivity=3)
    distance = ndimage.distance_transform_edt(binary)
    local_maxi = peak_local_max(distance, min_distance=min_distance, indices=False, labels=image_stack)
    markers = ndimage.label(local_maxi)[0]
    labeled_stack = watershed(-distance, markers, mask=binary)
    return labeled_stack

@exeTime
def properties_3d(labeled_stack):
    from MEHI.udf._moment import moment
    from scipy import ndimage as ndi
    import pandas as pd
    labeled_stack = np.squeeze(labeled_stack)
    prop = []
    columns = ('x', 'y', 'z', 'volume')
    indices = []
    label = 0
    objects = ndi.find_objects(labeled_stack)
    for i, _slice in enumerate(objects):
        if _slice is None:
            continue
        label += 1
        mu = moment(labeled_stack[_slice].astype(np.double))
        volume = mu[0]
        x = mu[1] + _slice[0].start
        y = mu[2] + _slice[1].start
        y = mu[3] + _slice[2].start
        prop.append([x,y,z,volume])
        indices.append(label)
    indices = pd.Index(indices, name='label')
    prop = pd.DataFrame(prop, index=indices, columns=columns)
    return prop

if __name__ == "__main__":
    pass
