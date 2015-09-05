################################
# Author   : septicmk
# Date     : 2015/09/05 16:57:42
# FileName : mha.py
################################

import numpy as np
import zlib
def _cast2int (l):
    l_new=[]
    for i in l:
        if i.is_integer(): l_new.append(int(i))
        else: l_new.append(i)
    return l_new

_shiftdim = lambda x, n: x.transpose(np.roll(range(x.ndim), -n))

def read_mha(fn):
    if fn.endswith('.mha'):
        
        f = open(fn,'rb')
        objecttype='2dimg' ## On default the matrix is considered to be an image
        direction_cosines = None
        offset = None
        spacing = None
        size = None
        data_type = None
        data = None
        compressed = False
        ## Read mha header
        for r in range(20):
            row=f.readline()
            if row.startswith('TransformMatrix ='):
                row=row.split('=')[1].strip()
                direction_cosines=_cast2int(map(float, row.split()))
            elif row.startswith('Offset ='):
                row=row.split('=')[1].strip()
                offset=_cast2int(map(float, row.split()))
            elif row.startswith('ElementSpacing ='):
                row=row.split('=')[1].strip()
                spacing=_cast2int(map(float, row.split()))
            elif row.startswith('DimSize ='):
                row=row.split('=')[1].strip()
                size=map(int, row.split())
                if len(size) < 3:
                    objecttype = '2dimg'
                else:
                    objecttype = '3dimg'
            elif row.startswith('ElementNumberOfChannels = 3'):
                data='vf' ## The matrix is a vf
                size.append(3)
            elif row.startswith('ElementType ='):
                data_type=row.split('=')[1].strip()
            elif row.startswith('CompressedData = True'):
                compressed = True
            elif row.startswith('ElementDataFile ='):
                break
        
        ## Read raw data
        data=''.join(f.readlines())
        f.close()
        if compressed:
            data = zlib.decompress(data)
        
        ## Raw data from string to array
        if data_type == 'MET_SHORT':
            data=np.fromstring(data, dtype=np.int16)
            data_type = 'short'
        if data_type == 'MET_UINT':
            data=np.fromstring(data, dtype=np.uint32)
            data_type = 'int'
        elif data_type == 'MET_FLOAT':
            data=np.fromstring(data, dtype=np.float32)
            data_type = 'float'
        elif data_type == 'MET_DOUBLE':
            data=np.fromstring(data, dtype=np.float64)
            data_type = 'double'
        elif data_type == 'MET_UCHAR':
            data=np.fromstring(data, dtype=np.uint8)
            data_type = 'uchar'

        print size
        ## Reshape array
        if objecttype == '2dimg':
            data=data.reshape(size[1],size[0])
        elif objecttype == '3dimg':
            data=data.reshape(size[2],size[1],size[0])
        elif objecttype == 'vf':
            data=data.reshape(size[2],size[1],size[0],3)
            data=_shiftdim(data, 3).T

        return data
    elif not fn.endswith('.mha'): ## Extension file is not ".mha". It returns all null values
        raise NameError('The input file is not a mha file!')


def write_mha (data, fn):
    if fn.endswith('.mha'):
        data = np.array(data, order = "C")
        size = data.shape
        data_type = data.dtype
        Ndim = data.ndim
        
        ## Check if the input matrix is an image or a vf
        if data.ndim == 2:
            objecttype='2dimg'
        elif data.ndim == 3:
            objecttype='img'
            size = (size[2],size[1],size[0])
        elif data.ndim == 4:
            objecttype='vf'
        
        f=open(fn, 'wb')
        ## Write mha header
        f.write('ObjectType = Image\n')
        f.write('NDims = '+str(Ndim)+'\n')
        #f.write('BinaryData = True\n')
        #f.write('BinaryDataByteOrderMSB = False\n')
        #f.write('CompressedData = False\n')
        #f.write('TransformMatrix = '+str(direction_cosines).strip('()[]').replace(',','')+'\n')
        #f.write('Offset = '+str(offset).strip('()[]').replace(',','')+'\n')
        #f.write('CenterOfRotation = 0 0 0\n')
        #f.write('AnatomicalOrientation = RAI\n')
        #f.write('ElementSpacing = '+str(spacing).strip('()[]').replace(',','')+'\n')
        f.write('DimSize = '+str(size).strip('()[]').replace(',','')+'\n')
        if data_type == np.uint16:
            f.write('ElementType = MET_SHORT\n')
        elif data_type == np.float32:
            f.write('ElementType = MET_FLOAT\n')
        elif data_type == np.uint32:
            f.write('ElementType = MET_UINT\n')
        elif data_type == np.float64:
            f.write('ElementType = MET_DOUBLE\n')
        elif data_type == np.uint8:
            f.write('ElementType = MET_UCHAR\n')
        f.write('ElementDataFile = LOCAL\n')
        
        ## Write matrix
        f.write(data)
        f.close()
        
    elif not fn.endswith('.mha'): ## File extension is not ".mha"
        raise NameError('The input file name is not a mha file!')

