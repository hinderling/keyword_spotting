from svgpathtools import svg2paths2, paths2svg
import numpy as np
from PIL import Image, ImageDraw
from skimage.filters import threshold_otsu
import cv2
import glob #get files with pattern matching
import os
import matplotlib.pyplot as plt

# Cut out single words from scan file and save them as individual files

# 1. import svg file and image
# 2. extract paths and turn into "filled" polygons, calculate bounding boxes
# 3. apply to imag
# 4. binarization 
# (optional/todo) 5. further preprocessing: normalization, tilting, ...
# 6. export as new file

pages = glob.glob("./images/*.jpg")
cutouts = glob.glob("./ground-truth/locations/*.svg")
pages.sort()
cutouts.sort()
for page,cutout in zip(pages,cutouts):
    page_number = os.path.splitext(os.path.basename(page))[0]
    paths, attributes, svg_attributes = svg2paths2(cutout)
    scan = cv2.imread(page, cv2.IMREAD_GRAYSCALE) #directly read in as grayscale
    for path, attribute in zip(paths,attributes):        
        #paths, attributes, svg_attributes = svg2paths2('270.svg')
        code = attribute['id']
        #https://github.com/mathandy/svgpathtools/blob/master/svgpathtools/paths2svg.py
        bbox = paths2svg.big_bounding_box(path) #returns (xmin, xmax, ymin, ymax)
        bbox = tuple(map(int,bbox)) #cast to int and convert back to tuple
        scan_crop = scan[bbox[2]:bbox[3],bbox[0]:bbox[1]]
        
        #binarize
        tresh = threshold_otsu(scan_crop) #https://scikit-image.org/docs/stable/api/skimage.filters.html#skimage.filters.threshold_otsu
        scan_crop_logic = scan_crop < tresh

        #create mask
        height = int(bbox[3]-bbox[2])
        width = int(bbox[1]-bbox[0])
        
        mask = Image.new('1', (width,height), "black")
        mask_draw = ImageDraw.Draw(mask)
        polygon = []
        for edge in path:
        #only add the first point of the lines, else we define points twice (a->b, b->c = b twice)
            polygon.append((int(edge.point(0).real)-bbox[0], int(edge.point(0).imag)-bbox[2])) #https://pillow.readthedocs.io/en/3.0.x/reference/ImageDraw.html
        #img = ImageDraw.Draw.rectangle(bbox, fill = 1, outline = 1) #white image the size of bbox
        mask_draw.polygon(polygon, fill="white", outline = None) #white mask in form of polygon

        img = np.logical_and(scan_crop_logic, mask)
        img = np.invert(img)
        img = img.astype(float)
        #squeeze all images into the same 120px height, but leave the length
        img = cv2.resize(src= img, dsize =(width,120),  interpolation = cv2.INTER_NEAREST)
        img = img > 0
        img = Image.fromarray(img)        
        filename = code       
        path = "./output/"+page_number        
        if not os.path.exists(path):
            os.mkdir(path)
        img.save(path+"/"+filename+".jpg")
    print("Done processing scan "+ os.path.basename(page))    
        
