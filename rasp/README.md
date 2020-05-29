# Raspberry Pi Squats app

The application to detect and count squats on Raspberry Pi.

Requirements:
- Raspbian 9. Stretch
- Python packages: numpy, flask, tensorflow, opencv
- trained CNN to classify poses (see NN folder of this repo)

Run:

python3 app.py

Workflow:

- check out setting in conf.py
- start the app
- open a page <app_host>:7000/
- you should see video stream and buttons start/stop for squats exercise
- fit your self in the camera frames and press start
- do some squats
- check out the squats count on the page
- taken frames are in <app_path>/frames. Clear them or use to re-train the network if needed. Leaving them for a long time leads to disk space exhausting.
