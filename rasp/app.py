from flask import Response, Flask, jsonify, request, send_from_directory, send_file
import logging
import os
import conf

if not os.path.isdir(conf.logpath):
    os.makedirs(conf.logpath)        

logging.basicConfig(filename=os.path.join(conf.logpath, conf.logfile),level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(threadName)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

import ctrl


app = Flask(__name__)

@app.route('/')
def main():
  return send_from_directory("static", "index.html")

@app.route('/version')
def index():
  return 'Squats detector 1.0'

@app.route('/status')
def status():
  return jsonify(ctrl.get_status())


@app.route('/start', methods=['POST'])
def start():
  rc, info = ctrl.start()
  if rc:
    return "ok", 200
  return "", 503
  

@app.route('/stop', methods=['POST'])
def stop():
  ctrl.stop()
  return "ok"
        
def generate():
  while True:
    rc, frame = ctrl.get_jpg()
    if rc and frame is not None:
      yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(frame) + b'\r\n')

@app.route("/stream")
def vstream():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000, debug=True, threaded=True, use_reloader=False)