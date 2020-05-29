import os
import sys
import cv2 as cv

target_size = 64

def resize_folder(inpath, outpath, size):
  if not os.path.isdir(outpath):
    os.makedirs(outpath)        

  for f in os.listdir(inpath):
    img = cv.imread(os.path.join(inpath, f), cv.IMREAD_GRAYSCALE)
    if img is None:
      continue
    i2 = cv.resize(img, size)
    cv.imwrite(os.path.join(outpath, f), i2)
    print (f)
  



inpath = sys.argv[1]
outpath = sys.argv[2]
resize_folder(inpath, outpath, (target_size, target_size))