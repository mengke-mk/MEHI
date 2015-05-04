################################
# Author   : septicmk
# Date     : 2015/3/27 9:17:17
# FileName : MEHI_filter.py
################################

import numpy as np
import pandas as pd

class Spatial_Filter:
    
    def __init__(self):
        pass
    
    def get_per(self, sli):
        '''
        Usage:
         - get the bounding box's size and the perimeter
        Args:
         - sli: the slice of a object
        Return:
         - x: width
         - y: height
         - per: perimeter 
        '''
        xz, yz = sli.shape
        x = sum(np.clip(sum(sli), 0, 1))
        y = sum(np.clip(sum(sli.T), 0, 1))
        for i in range(1,xz-1):
            for j in range(1,yz-1):
                if sum(sli[i-1:i+1,j-1:j+1].flatten()) == 9:
                    sli[i][j] = 0
        return x, y , sum(sli.flatten()) 
        
    def get_feature(self, cmap):
        '''
        Usage:
         - get the surface to volume rate and the anisotropy rate
        Args:
         - cmap: labeled 3d image
        Returns:
         - features: the list of (surface/volume, anisotropy)
        '''
        num = max(cmap.flatten())
        features = []
        for i in range(1,num):
            tmp = map(lambda x: 1 if x==i else 0, cmap)
            lx, ly ,lz = cmap.shape
            x, y, z = 0,0,0
            vol = 0
            sur = 0
            for j in range(lz):
                if sum(cmap[j].flatten):
                    z += 1
                    if z != 1:
                        vol += sum(cmap[j].flatten ^ cmap[j-1].flatten)
                    else:
                        vol += sum(cmap[j].flatten)
                    px, py, delta = get_per(camp[j])
                    x, y = max(x,px), max(y,py)
                    sur += delta
            con = (.0+sur)/vol
            ani = max(x,y,z)/(min(x,y,z)+.0)
            features.append((con,ani))
        return features
    
    def main(self, cmap, cell_table, threshold):
        '''
        Usage:
         - filter the object which do not match the shape of nuclei
        Args:
         - cmap: labeled 3d image
         - cell_table: the info of the cell
         - threshold : the preset threshold to describe a nuclei
        Returns:
         - cmap: input after filtering
         - cell_table : input after filtering
        '''
        features = get_feature(cmap)
        jud = []
        trans = [0]
        cnt = 0
        for con, ani in features:
            cnt += 1
            if con <= threshold[0] and ani <= threshold[1]:
                jud.append(cnt)
                trans.append(cnt)
            else: trans.append(0)
            
        cell_table['new_label'] = jud
        properties.set_index('new_label', drop=True, append=False, inplace=True)
        properties.index.name = 'label'
        cmap = trans[cmap]
        return cmap, cell_table

if __name__ == '__main__':
    pass
            
