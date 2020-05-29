import sys
import numpy as np
import os
import cv2 as cv
from time import time
import conf
import logging

if __name__ == '__main__':
  logging.basicConfig(filename="test_cls.log",level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

import tensorflow as tf

model = None
graph = None

def init():
    t = time()
    global model, graph
    f = open(conf.model_json, 'r')
    model_data = f.read()
    f.close()

    model = tf.keras.models.model_from_json(model_data)
    model.load_weights(conf.model_h5)
    graph = tf.get_default_graph()
    t = time() - t
    logging.debug(("Loaded model in {:.4f} sec".format(t)))

def classify(g):
    global model, graph
    t = time()
    g1 = np.reshape(g,[1, conf.mask_size, conf.mask_size,1])
    c = None
    with graph.as_default():
        c = model.predict_classes(g1)

    t = time() - t
    logging.debug(("Classified in {:.4f} sec".format(t), c))
    
    return c[0] if c else None


if __name__ == '__main__':
  init()
  path = sys.argv[1]
  if os.path.isdir(path):
    for f in os.listdir(path):
      img = cv.imread(os.path.join(path, f), cv.IMREAD_GRAYSCALE)
      if img is None:
        continue
      c = classify(img)
      print ("Classified", f, c)
  else:
    img = cv.imread(path, cv.IMREAD_GRAYSCALE)
    c = classify(img)
    print ("Classified", path, c)


     
