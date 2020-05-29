import os
from datetime import datetime
import time
import logging
import cv2 as cv
import conf
import squeue

outpath = conf.frames_path
test_path = conf.root + "test_data"

if not os.path.isdir(outpath):
  os.makedirs(outpath)        


captur = None
flist = None
findex = -1

def get_jpg():
  global captur, flist, findex
  if flist is None:
    return False, None
  if findex >= len(flist) or findex < 0:
    return False, None
  print ("GetJpg", findex, flist[findex])
  frame = cv.imread(flist[findex])
  if frame is None:
    return False, None
  name = "{0}/{1}/{2:03d}.jpg".format(outpath, captur, findex + 1)
  rc = cv.imwrite(name, frame)
  squeue.push(name, captur)
  findex += 1
  return cv.imencode(".jpg", frame)



def start_capture(quid):
  global captur, flist, findex
  if captur is not None:
    return False, None
  captur = quid
  os.makedirs(outpath + "/" + captur)
  findex = 0
  flist = [os.path.join(test_path, f) for f in os.listdir(test_path)]
  flist.sort()
  print(flist)

  return True, captur


def stop_capture():
  logging.debug("Stop capture")
  global captur
  captur = None
