import numpy as np
from scipy import ndimage as ndi
from skimage import measure
import scipy.misc
from PIL import Image
from skimage.morphology import medial_axis
from skimage.morphology import skeletonize
from skimage.morphology import medial_axis
from scipy import ndimage as ndi
from skimage.morphology import medial_axis
import matplotlib.pyplot as plt
from itertools import groupby
import gdal
import operator
from osgeo import gdal, gdalnumeric, ogr, osr
import ogr
from PIL.Image import core as Image
from PIL import ImageDraw
import operator
from functools import reduce
import seaborn as sns
import sys
import os
import importlib



def main():
    script = sys.argv[0]
    filename_in = sys.argv[1] # file name of masked .tif 0: no water, 1: water.

    ds_water = gdal.Open(filename_in)

    img_water = np.array(ds_water.GetRasterBand(1).ReadAsArray())

    img_water[img_water<0] =0
    pot_r_labels = measure.label(img_water, background=0)  # identifies connected components and groups them, assigning a group the same integer
    num_potars = np.amax(pot_r_labels)  # tell how many potential rivers are  each timestep by taking the maximum group integer
    pot_r_array= np.asarray(pot_r_labels)  # make the potential rivers matrix an array
    temp_pot_r_array = pot_r_array.copy()
    temp_pot_r_array_int = np.int8(pot_r_labels)


    attributes = measure.regionprops(temp_pot_r_array_int, intensity_image=img_water)
    r_length = []
    r_width = []
    r_centroid = []
    r_perimeter = []
    r_area = []



    for i in range(0, len(attributes)):
        r_length.append(attributes[i].major_axis_length)
        r_width.append(attributes[i].minor_axis_length)
        r_centroid.append(attributes[i].centroid)
        r_perimeter.append(attributes[i].perimeter)
        r_area.append(attributes[i].filled_area)



    lengths = np.asarray(r_length)
    widths = np.asarray(r_width)
    perimeters = np.asarray(r_perimeter)
    area = np.asarray(r_perimeter)

    # find the segment with the longest length, use this to calculate width
    length_max = np.max(lengths)
    max_loc = np.asarray([i for i, j in enumerate(lengths) if j == length_max])
    temp_pot_r_array_int[temp_pot_r_array_int<=max_loc ] = 0
    temp_pot_r_array_int[temp_pot_r_array_int>max_loc + 1] = 0
    # finds the medial axis along the segment, and calculates the distance
    skel, dist = medial_axis(temp_pot_r_array_int, return_distance=True)
    # calculates width
    dist_on_skel = dist * skel

    # using max or mean width
    out_dist = np.round((np.max(dist)),2)

    print(out_dist)

    return  out_dist

main()


