from keras.models import Sequential, Model
from keras.layers import Conv2D, Convolution2D
from keras.layers import Input
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense
from keras.layers import Activation
from keras.layers import BatchNormalization
from keras.layers import Dropout
from keras.optimizers import SGD
from keras.optimizers import Adam


import numpy as np
from keras.preprocessing.image import ImageDataGenerator

size = 64

def createModel(input_shape, cls_n ):
    model = Sequential([
        Convolution2D(8,(5,5), activation='relu', input_shape=input_shape),
        MaxPooling2D(),
        Flatten(),
        Dense(512, activation='relu'),
        Dense(cls_n, activation='softmax')
      ])

    opt = SGD(lr=0.01)

    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
    return model



input_shape = (size, size, 1)

EPOCHS = 30
INIT_LR = 1e-3
cls_n = 3

model = createModel(input_shape, cls_n)

train_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory("data", color_mode="grayscale", target_size = (size, size), batch_size = 32, class_mode = 'categorical')
label_map = (training_set.class_indices)
print (label_map)

model.fit_generator(training_set, steps_per_epoch = 5, epochs = EPOCHS, validation_steps = 3)

print (label_map)

model_json = model.to_json()
with open("./model.json","w") as json_file:
  json_file.write(model_json)

model.save_weights("./model.h5")