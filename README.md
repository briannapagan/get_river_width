# get_river_width
Find the river width (and other properties) from a masked water image

get_river_width.py filename.tif

input:    .tif file with region already masked for water. 0: no water, 1: water. 

output:   maximum width (pixel count) along the river

https://scikit-image.org/docs/dev/api/skimage.measure.html#skimage.measure.regionprops
scikit-image by default provides estimates of length and width (referred to as major/minor axis), however, this is calcuated as "the length of the major axis of the ellipse that has the same normalized second central moments as the region." For a winding river system, this is not accurate. From scikit-image, this code first identifies the longest designated water body (if more than one river in the image, this can easily be adapted). Then using scikit-image medial axis function, the river is skelatonized and the distance from the river edge calculated along the medial axis. 

Questions? Contact: briannapagan@gmail.com 
