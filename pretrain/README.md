# Pretrain
## Preprocess image data to train CNN for squats detection
1. Copy prepare.py from ../rasp folder
2. Create input folder and put a folder with images into it
3. python3 pretrain.py
4. It will show grayscale pictures with bounding rects. Classify the pic with pressing: 
    - S for stand
    - Q for squat
    - N for nothing
5. When all the pictures handled they will be moved into "raw" folder. The classified masks will be put into "train" folder
6. Copy "train" folder into train data of CNN and re-train the model
