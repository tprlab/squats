# Squats detector with OpenCV and Tensorflow

This repo stores component for squats detection and counting

There are 3 parts:

- Application (rasp) to be run on Raspberry Pi. Takes shots from camera, extracts masks, classifed the masks, decides was it squat or not.

  [App intstructions](https://github.com/tprlab/squats/rasp)
- Pretrain - a GUI app to annotate (manually classify the pictures)

  [Labeling instructions](https://github.com/tprlab/squats/pretrain)
- Neural network - an app to train a CNN on the pictures

  [Train CNN instructions](https://github.com/tprlab/squats/nn)

