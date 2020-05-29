import cv2 as cv
import numpy as np
import conf

rect = None
backSub = None
first = True

def adjust_rect(rect, r):
  if rect[0] is None:
    for i in range(4):
      rect[i] = r[i]
    return
  rect[0] = min(rect[0], r[0])
  rect[1] = min(rect[1], r[1])
  rect[2] = max(rect[2], r[2])
  rect[3] = max(rect[3], r[3])
    

def cut_mask(img, rect, outpath = None, dbg_path = None):
  kernel = None
  img = cv.dilate(img, kernel, 3)

  cnts, hierarchy = cv.findContours(img, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE)

  if len(cnts) < 1:
    return None
  areas = [cv.contourArea(c) for c in cnts]
  mx = np.argmax(areas)
  C = cnts[mx]

  x,y,w,h  = cv.boundingRect(C)
  adjust_rect(rect, (x,y, x + w, y + h))
  cut = img[rect[1] : rect[3], rect[0] : rect[2]]
  dimg = img
  if not dbg_path is None:
    dimg = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
    cv.drawContours(dimg, cnts, mx, (0,0,255), 3)
    cv.rectangle(dimg,(rect[0],rect[1]),(rect[2], rect[3]),(0,255,0),2)
    cv.rectangle(dimg,(x,y),(x + w, y + h),(255,0,0),2)
    cv.imwrite(dbg_path, dimg)

  r, cut = cv.threshold(cut, 0 ,255,cv.THRESH_BINARY | cv.THRESH_OTSU)
  cut = cv.medianBlur(cut, 5)
  w = rect[2] - rect[0]
  h = rect[3] - rect[1]
  size = max(w,h)
  x_offset = int((size - w) / 2)
  y_offset = int((size - h) / 2)
  q = np.zeros((size,size), np.uint8)
  q[y_offset : y_offset + h, x_offset : x_offset + w] = cut
  q = cv.resize(q, (conf.mask_size, conf.mask_size))
  if outpath:
    cv.imwrite(outpath, q)
  return q


def init():
  global rect, backSub, first
  rect = [None, None, None, None]
  backSub = cv.createBackgroundSubtractorMOG2()
  first = True


def handle(frame, outpath = None, dbgpath = None):
  global rect, backSub, first
  if backSub is None:
    return None

  mask = backSub.apply(frame)
  if first:
    first = False
    return None

  return cut_mask(mask, rect, outpath, dbgpath)

