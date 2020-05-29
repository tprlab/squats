import os

import time
import logging
import cv2 as cv
import conf
import squeue

outpath = conf.frames_path

if not os.path.isdir(outpath):
  os.makedirs(outpath)        

vs = cv.VideoCapture(0)

captur = None
cnt = 1
limit = 100

def get_jpg():
  global captur, cnt
  rc, frame = vs.read()
  if rc and (captur is not None):
    tcnt = cnt + 1 
    name = "{0}/{1}/{2:03d}.jpg".format(outpath, captur, tcnt)
    rc = cv.imwrite(name, frame)
    logging.debug(("saved", name, rc))
    if not squeue.push(name, captur):
      logging.error(("Cannot push", name, "to", captur))
      return

    cnt = tcnt
    if cnt >= limit:
      captur = None 
      logging.debug("Capture canceled due to limit")

  return cv.imencode(".jpg", frame)


def start_capture(id):
  global captur, cnt
  if captur is not None:
    return False
  logging.debug("Start capture")
  cnt = 0
  #captur = datetime.now().strftime('%Y%m%d-%H%M%S')
  captur = id
  os.makedirs(outpath + "/" + captur)
  return True

def count():
  return cnt

def stop_capture():
  logging.debug("Stop capture")
  global captur
  captur = None
  return cnt
       

if __name__ == '__main__':
  logging.basicConfig(filename="frames.log",level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
  rc = start_capture()
  print ("Started", rc)
  for i in range(3):
    print (i)
    time.sleep(1)
  stop_capture()
