from osgeo import gdal
import numpy as np
from tqdm import trange
import os
from os import listdir
import os
# os.environ['PROJ_LIB'] = r'D:\software\anaconda3\install\envs\PyTorch39\Lib\site-packages\pyproj\proj_dir\share\proj'


def write_tiff(filename, im_proj, im_geotrans, im_data, binary=False):
    """ save as tiff"""

    if 'int8' in im_data.dtype.name:
        datatype = gdal.GDT_Byte
    elif 'int16' in im_data.dtype.name:
        datatype = gdal.GDT_UInt16
    else:
        datatype = gdal.GDT_Float64

    if binary:
        im_data[im_data == 1] = 255
        im_bands, (im_height, im_width) = 1, im_data.shape  # 用来分割标注好的单波段影像的代码
    else:
        im_bands, im_height, im_width = im_data.shape  # 用来分割三波段影像的代码
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(filename, im_width, im_height, im_bands, datatype)

    dataset.SetGeoTransform(im_geotrans)
    dataset.SetProjection(im_proj)

    if binary:
        dataset.GetRasterBand(1).WriteArray(im_data)  # 用来分割标注好的单波段影像的代码
    else:
        for i in range(im_bands):  # 用来分割三波段影像的代码
            dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
        del dataset

# 选择文件夹
filepath = r'E:\YXJC\tiff\\'
pathdir = r'E:\YXJC\ImageSplit\\'

w0 = 30720
h0 = 30720
w = 512
h = 512
k = int(w0 / w)
k1 = int(h0 / h)
count = 0
for dir in os.listdir(filepath):
    files = filepath + dir
    dataset = gdal.Open(files)
    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize
    geotrans = dataset.GetGeoTransform()
    im_proj = dataset.GetProjection()
    loc = [w, h]
    for i in trange(k):
        for j in range(k1):
            im_geotrans = (geotrans[0] + i * loc[0]/2, 0.5, 0.0, geotrans[3] - j * loc[1]/2, 0.0, -0.5)
            im_data = dataset.ReadAsArray(i * loc[0], j * loc[1], loc[0], loc[1])
            path = pathdir + f'{count * k * k + i * k + j}.tif'
            # print(path)
            write_tiff(path, im_proj, im_geotrans, im_data)
    count += 1

"""count = 0
for dir in listdir(filepath):
    dataset=gdal.Open(filepath+dir)
    im_width = dataset.RasterXSize
    im_height = dataset.RasterYSize
    geotrans = dataset.GetGeoTransform()
    im_proj = dataset.GetProjection()

    loc = [512,512]


    for i in range(15):
        for j in range(15):
            im_geotrans = (geotrans[0]+i*loc[0],1.0,0.0,geotrans[3]-j*loc[1],0.0,-1.0)
            im_data = dataset.ReadAsArray(i*loc[0],j*loc[1],loc[0],loc[1])
            # im_data[im_data==1]=255
            path = pathdir + f'{count*225+i*15+j}.tif'
            # print(im_data)
            write_tiff(path,im_proj,im_geotrans,im_data,False)
    count = count + 1
"""

# file = './data/split_test/1.tif'


# dataset=gdal.Open(file)
# im_width = dataset.RasterXSize
# im_height = dataset.RasterYSize
# geotrans = dataset.GetGeoTransform()
# im_proj = dataset.GetProjection()

# loc = [512,512]

# im_geotrans = (geotrans[0]+loc[0]/2,0.5,0.0,geotrans[3]-loc[1]/2,0.0,-0.5)
# im_data = dataset.ReadAsArray(loc[0],loc[1],loc[0],loc[1])
# path = './data/split_test/1-1.tif'
# write_tiff(path,im_proj,im_geotrans,im_data,False)
