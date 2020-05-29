import cv2 as cv
import os
from datetime import datetime
import shutil
import numpy as np
import prepare

INPUT_PATH = "input/"
OUT_PATH = "raw"
TARGET_PATH = "train"
DBG_TMP = "dbg_tmp.jpg"

if not os.path.isdir(OUT_PATH):
  os.makedirs(OUT_PATH)        

def create_sub_folders(path, subs):
  for p in subs:
    fp = os.path.join(path, p)
    if not os.path.isdir(fp):
        os.makedirs(fp)        


def create_prep_folders(path):
  paths = ["squat", "stand", "noth", "mask/stand", "mask/squat", "mask/noth", "dbg/stand", "dbg/squat", "dbg/noth"]
  create_sub_folders(path, paths)


def handle_folder(path):
  create_prep_folders(path)

  prepare.init()

  for f in os.listdir(path):
    fpath = os.path.join(path, f)
    if os.path.isdir(fpath):
      continue
    frame = cv.imread(fpath);

    mask = prepare.handle(frame, None, DBG_TMP)
    if mask is None:
      continue

    dbg = cv.imread(DBG_TMP)
    cv.imshow("Image", dbg)
    k = cv.waitKey(0)
    target = "noth"
    if k == 27:
      break
    elif k == ord('s'):
      target = "stand"
    elif k == ord('q'):
      target = "squat"

    print ("Copy", fpath, "to", target)
    cv.imwrite(os.path.join(path, "mask", target,f), mask)
    dbgpath = os.path.join(path, "dbg", target, f) if target[0] == "s" else None
    if dbgpath is not None:
      cv.imwrite(dbgpath, dbg)


def copy_mask_folder(path, src, target):
  if not os.path.isdir(path):
    return
  for f in os.listdir(path):
    fname = "{0}-{1}".format(src, f)
    shutil.copy(os.path.join(path, f), os.path.join(target, fname))

def copy_masks(fpath, src):
  create_sub_folders(TARGET_PATH, ["n", "s", "q"])
  copy_mask_folder(os.path.join(fpath, "mask/noth"), src, os.path.join(TARGET_PATH, "n"))
  copy_mask_folder(os.path.join(fpath, "mask/squat"), src, os.path.join(TARGET_PATH, "q"))
  copy_mask_folder(os.path.join(fpath, "mask/stand"), src, os.path.join(TARGET_PATH, "s"))

for f in os.listdir(INPUT_PATH):
  fpath = os.path.join(INPUT_PATH, f)
  if not os.path.isdir(fpath):
    continue

  handle_folder(fpath)

  copy_masks(fpath, f)
  shutil.move(fpath, os.path.join(OUT_PATH, f))


