# @Author: Абделлах Улахияне
# @Date:   2021-04-17 23:54:50
# @Last Modified by:   Абделлах Улахияне
# @Last Modified time: 2021-04-18 06:47:44

# Importing the Keras libraries and packages
import tensorflow as tf
from tensorflow import keras
import keras
from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

import sys
import os
from config import *

#chaeck if data are already collected or not
if not os.path.isdir("data")          or  \
   not os.path.isdir("data/training") or  \
   not os.path.isdir("data/testing")  or  \
   not os.path.isdir("data/validation") :
        print("Exiting : ExCollect Data first")
        exit(1)


#  1 - Building the CNN
#------------------------------
# Initializing the CNN
classifier = Sequential()
# First convolution layer and pooling
classifier.add(Convolution2D(32, (3, 3), input_shape=(image_size[0], image_size[1], 1), activation='relu'))
classifier.add(MaxPooling2D(pool_size=(2, 2)))
# Second convolution layer and pooling
classifier.add(Convolution2D(32, (3, 3), activation='relu'))
# input_shape is going to be the pooled feature maps from the previous convolution layer
classifier.add(MaxPooling2D(pool_size=(2, 2)))
# Flattening the layers
classifier.add(Flatten())
# Adding a fully connected layer
classifier.add(Dense(units=128, activation='relu'))
#                                                              softmax for more than 2 class's
classifier.add(Dense(units=len(os.listdir('./data/training/')), activation='softmax')) 
# Compiling the CNN
#                                 categorical_crossentropy for more than 2 class's
classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) 
#  2 - Preparing the train/test data and training the model
train_datagen = ImageDataGenerator(
        rescale=1./255,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)
training_set = train_datagen.flow_from_directory('data/training',
                                                 target_size=image_size,
                                                 batch_size=batch_size,
                                                 color_mode='grayscale',
                                                 class_mode='categorical')
test_set = test_datagen.flow_from_directory('data/testing',
                                            target_size=image_size,
                                            batch_size=batch_size,
                                            color_mode='grayscale',
                                            class_mode='categorical') 
#.fit_generator will be dupricated in next version of keras
classifier.fit(#_generator(
        training_set,
        # No of images in training set
        steps_per_epoch=3, 
        epochs=epochs,
        validation_data=test_set,
        # No of images in test set
        validation_steps=30)
#check if model foler exist or not and make it if does not exist
if not os.path.isdir("modeles"):
        os.mkdir("modeles")
# Saving the model as json
model_json = classifier.to_json()
with open("modeles/model.json", "w") as json_file:
    json_file.write(model_json)
#saving model weights
classifier.save_weights('modeles/model.h5')

