import frames
import squats
import squeue
from datetime import datetime
import logging
#import test_frames as frames

sq_id = None

status = -1;
squats_n = 0
frames_n = 0
processed = 0

def start():
  global sq_id, status
  status = -1
  qid = squeue.getQid()
  if qid is not None:
    logging.error(("Cannot start new sequnce because active is ", qid))
    return False, "Busy"

  qid = datetime.now().strftime('%Y%m%d-%H%M%S')
  if not squeue.acquire(qid):
    logging.error(("Cannot aquire queue"))
    return False, "Acquire"

  if not frames.start_capture(qid):
    logging.error(("Cannot start frames capture"))
    return False, "Capture"

  if not squats.begin(qid):
    logging.error(("Cannot start squats detector"))
    return False, "Squats"

  sq_id = qid
  status = 0
  squats_n = 0
  processed = 0
  frames_n = 0
  return True, qid

def stop():
  global total
  frames_n = frames.stop_capture()
  if squeue.release(sq_id, onEmptyQ):
    onEmptyQ()


def get_jpg():
  return frames.get_jpg()

def onEmptyQ():
  global status, squats_n, sq_id
  status = 1
  squats_n = squats.count()
  squats.end()
  logging.debug(("Q released", sq_id))
  sq_id = None

def get_status():
  global squats_n, frames_n, processed
  squats_n = squats.count()
  frames_n = frames.count()
  processed = squats.processed()
  return {"status" : status, "squats" : squats_n, "frames" : frames_n, "processed" : processed}