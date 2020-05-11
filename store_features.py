import numpy as np
import matplotlib.pyplot as plt
import pickle
import os
import time
import sys

def main():
  t0 = time.time()
  
  ########## get name of all pictures in "cutouts_png" ###########
  picture_names = {}
  for page in os.listdir("data/cutouts_png/"):
    # get all names of the pictures and cut off the suffix (".png"); they are
    # needed to name the keys of the dictionary later on
    picture_names[page] = [name[:-4] for name in
                           os.listdir("data/cutouts_png/" + page + "/")]
  
  ########## read all pictures ###########
  print("reading pictures...")
  # store all images as numpy arrays
  pictures = {}
  for page in picture_names:
    for pic_name in picture_names[page]:
      path_to_pic = "data/cutouts_png/" + page + "/" + pic_name + ".png"
      pictures[pic_name] = np.array(plt.imread(path_to_pic))
  
  ########## get features of all pics ###########
  print("calculating features...")
  featureDict = {}
  for i, picName in enumerate(pictures):
    sys.stdout.write('\r')
    sys.stdout.write('picture {}/{}'.format(i+1, len(pictures)))
    sys.stdout.flush()
    featureDict[picName] = get_features(pictures[picName])
  print()

  ########## pickle-dump the dict ###########
  print("dumping features in binary file...")
  with open("dictPickle.bin", "wb") as dictionary_file:
    pickle.dump(featureDict, dictionary_file)
  print("finished dumping")
  
  ########## print time ###########
  tot_time = time.time()-t0
  minutes = int(tot_time/60)
  seconds = int(tot_time - (minutes*60))
  print("time: ", minutes, "min ", seconds, "s", sep="")
 


def get_features(img):
  # lists: UC, LC, b/w-ratio, b/w-ratio between UC and LC, center of black pixels
  upper, lower, bw_ratio = [], [], []
  bw_ratio_UC_to_LC, black_center, transes = [], [], []
  
  width = np.shape(img)[1]
  height = np.shape(img)[0]
  
  # iterate over all columns
  for col in range(width):
    
    trans_count = 0
    for px in range(height-1): # -1 to not overshoot, cause we compare with i+1
      if img[px,col] != img[px+1,col]:
        trans_count += 1
    ### transitions
    transes.append(trans_count)
    
    black_pxls = np.where(img[:,col] == 0)[0]
    ### b/w-ratio
    bw_ratio.append(len(black_pxls) / height)
    
    # to avoid 0-divisions and define what happens if a column has no black pixel
    if len(black_pxls) != 0:
      ### UC
      upper.append(black_pxls[0])
      
      ### LC
      lower.append(black_pxls[-1])
      
      # n_black_pixels / n_pixels between UC and LC
      n_total = len(img[upper[-1]:lower[-1]+1, col])
      ### b/w-ratio between UC and LC
      bw_ratio_UC_to_LC.append(len(black_pxls) / n_total)
      
      ### center of black pixels
      black_center.append(np.sum(black_pxls) / len(black_pxls))
      
    # if no black pixels: append '0' to the features below
    else:
      ### b/w-ratio between UC and LC
      bw_ratio_UC_to_LC.append(0)
      
      ### center of black pixels
      black_center.append(0)
      
  retDict = {"UC": upper, "LC": lower, "bw_ratio": bw_ratio,
             "bw_ratio_UC_to_LC": bw_ratio_UC_to_LC, "black_center": black_center,
             "transitions": transes}
  return retDict


if __name__ == "__main__":
  main()
