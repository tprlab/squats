import queue
import logging

Q = queue.Queue()
qid = None
released = False
rcallback = None

def getQid():
  return qid

def acquire(_id):
  global qid
  if not qid is None:
    logging.debug(("Q denied aquire ", _id, "because of", qid))
    return False
  qid = _id
  logging.debug(("Q aquired by ", _id))
  released = False
  return True

def release(_id, callback = None):
  global qid, released, rcallback
  released = True

  if not Q.empty():
    logging.debug(("Q deffered release", qid))
    rcallback = callback    
    return False

  qid = None
  logging.debug(("Q released imediately", qid))
  return True

def empty():
  return Q.empty()

def push(a, _id):
  if qid != _id:
    return False
  Q.put(a)
  return True

def pop(_id):
  global qid, released
  if released:
    if Q.empty():
      logging.debug(("Q released ", qid))
      qid = None
      if rcallback:
        rcallback()

  return Q.get()
