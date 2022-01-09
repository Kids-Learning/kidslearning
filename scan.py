import argparse
import cv2
import numpy as np
from numpy import genfromtxt
import csv
import operator
from keras.models import load_model
from functions import clean, read_transparent_png
model = load_model("model.h5")

# cv2.waitKey(0)

def predict():

    # impath = "K:\\DDD CHAR RECOGNI\\new\\malayalam-character-recognition-master (3)\\malayalam-character-recognition-master\\2_1_3.jpg"


    impath = "C:\\Users\\user\\Desktop\\project\\Kids Learning\\static\\writings\\test.bmp"
    image = cv2.imread(impath, cv2.COLOR_GRAY2RGB)

    if image.shape[2] == 4:
        image = read_transparent_png(impath)
    img = clean(image)
    image_data = img
    dataset = np.asarray(image_data)
    dataset = dataset.reshape((-1, 32, 32, 1)).astype(np.float32)
    print(dataset.shape)
    a = model.predict(dataset)[0]

    classes = np.genfromtxt('classes.csv', delimiter=',')[:, 1].astype(int)

    print(classes)
    new = dict(zip(classes, a))
    res = sorted(new.items(), key=operator.itemgetter(1), reverse=True)

    print("#########***#########")
    print("Imagefile = ", impath)
    print("Character = ", int(res[0][0]))
    print("Confidence = ", res[0][1] * 100, "%")
    if 1==1:
        print("Other predictions")
        for newtemp in res:
            print("Character = ", newtemp[0])
            print("Confidence = ", newtemp[1] * 100, "%")

    print("character code",res[0][0])
    return int(res[0][0])

