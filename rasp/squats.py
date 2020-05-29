import squeue
import threading
import conf
import cv2 as cv
import prepare
import logging
import os
import os.path as fs
import sys

if __name__ == '__main__':
  logging.basicConfig(filename="logs/squats.log",level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


import detect

done = False
sq_id = None
sq_cnt = -1
ended = False
frames_cnt = 0

dbg_path = conf.root + "/dbg"

if not os.path.isdir(dbg_path):
  os.makedirs(dbg_path)        

STAND = 2
SQUAT = 1

state = 0
T = None

def squat_detected():
  print ("Squat detected")
  global sq_cnt
  sq_cnt += 1

def handle_cls(cls):
  global state
  if cls == STAND:
    if state == 0:
      state = STAND
    elif state == SQUAT:
      state = STAND
      squat_detected()
  elif cls == SQUAT:
    if state == STAND:
      state = SQUAT

def handle_img(path):
  img = cv.imread(path)
  if img is None:
    logging.debug(("Cannot read", path))
    return None
  fname = fs.basename(path)
  mask = prepare.handle(img, fs.join(dbg_path, "out_" + fname),fs.join(dbg_path, "dbg_" + fname))
  if mask is None:
    logging.debug(("no mask for", path))
    return None
  
  cls = detect.classify(mask)
  logging.debug(("Classified", path, cls))
  print("Cls", path, cls)
  handle_cls(cls)
  return cls
        
     
def qloop():
  detect.init()
  global done, sq_id, frames_cnt

  prev = None
  while not done:
    name = squeue.pop(sq_id)
    if sq_id is None:
      prev = sq_id
      continue
    if prev is None:
      logging.debug(("Begin", sq_id)) 
      prepare.init()
      
    prev = sq_id
    cls = handle_img(name)
    frames_cnt += 1


def stop_loop():
  global done, T
  print ("Stopping")
  done = True
  if T:
    T.join()
    T = None


def begin(_id):
  global sq_id, sq_cnt, frames_cnt
  if sq_id:
    return False
  sq_id = _id
  sq_cnt = 0
  frames_cnt = 0
  ended = False
  return True
  

def end():
  global ended, sq_id
  ended = True
  sq_id = None


def count():
  return sq_cnt

def processed():
  return frames_cnt

if __name__ == "__main__":
  test_folder = sys.argv[1] if len(sys.argv) > 1 else "test_data"
  detect.init()
  prepare.init()
  flist = [f for f in os.listdir(test_folder)]
  flist.sort()

  for f in flist:
    handle_img(os.path.join(test_folder, f))
else:
  T = threading.Thread(target=qloop)
  T.daemon = True
  T.start()
