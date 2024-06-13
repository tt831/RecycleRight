import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import streamlit as st
import numpy as np
import tempfile
import pandas as pd
from datetime import datetime
import time
# import tensorflow as tf
# import core.utils as utils
# from core.yolov4 import filter_boxes
# from core.functions import *
# from tensorflow.python.saved_model import tag_constants
# from PIL import Image

video = cv2.VideoCapture(0)
labels = []

def get_object(x):
    item = x
    if item == "paper":
        st.write("Paper is recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "bottle":
        st.write("Bottles are recyclable! You can recycle it in the blue bin.")
        st.write("Steps to recycle:")
        st.write("1. Empty the bottle, and remove the cap.")
        st.write("2. Rinse the bottle, and remove any labels.")
        st.write("3. Put the bottle in the blue bin, and you're done!")
    elif item == "can":
        st.write("Cans are recyclable! You can recycle it in the blue bin.")
        st.write("Steps to recycle:")
        st.write("1. Empty the can, and remove the label.")
        st.write("2. Rinse the can.")
        st.write("3. Put the can in the blue bin, and you're done!")
    elif item == "plastic":
        st.write("Plastic is recyclable! You can recycle it in the blue bin.")
        st.write("Steps to recycle:")
        st.write("1. Empty the plastic, and remove any labels if required.")
        st.write("2. Rinse the plastic, making sure any residue is removed.")
        st.write("3. Put the plastic in the blue bin, and you're done!")
    elif item == "cardboard":
        st.write("Cardboard is recyclable! You can recycle it in the blue bin.")
        st.write("Steps to recycle:")
        st.write("1. Flatten the cardboard, and remove any tape.")
        st.write("2. Put the cardboard in the blue bin, and you're done!")
    elif item == "newspapers" or item == "newspaper":
        st.write("Newspapers are recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "books" or item == "book":
        st.write("Books are recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "magazines" or item == "magazine":
        st.write("Magazines are recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "envelope" or item == "envelopes":
        st.write("Envelopes are recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "glass":
        st.write("Glass is recyclable! You can recycle it in the blue bin.")
        st.write("Steps to recycle:")
        st.write("1. Empty the glass, and remove any labels.")
        st.write("2. Rinse the glass.")
        st.write("3. Put the glass in the blue bin, and you're done!")
    elif item == "metal":
        st.write("Metal is recyclable! You can recycle it in the blue bin.")
        st.write("Steps to recycle:")
        st.write("1. Empty the metal, and remove any labels.")
        st.write("2. Rinse the metal. Make sure it isn't rusty!")
        st.write("3. Put the metal in the blue bin, and you're done!")
    else:
        st.write("This item is probably not recyclable, please dispose of it in the correct bin, or check at the link below!")
        st.write("[Items that can be recycled](https://www.nea.gov.sg/docs/default-source/our-services/waste-management/list-of-items-that-are-recyclable-and-not.pdf)")

def get_object2(x, result):
    item = x
    if item == "paper":
        return("Paper is recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "bottle":
        return("Bottles are recyclable! You can recycle it in the blue bin.\nSteps to recycle:\n1. Empty the bottle, and remove the cap.\n2. Rinse the bottle, and remove any labels.\n3. Put the bottle in the blue bin, and you're done!")
    elif item == "can":
        return("Cans are recyclable! You can recycle it in the blue bin.\nSteps to recycle:\n1. Empty the can, and remove the label.\n2. Rinse the can.\n3. Put the can in the blue bin, and you're done!")
    elif item == "plaresultic":
        return("Plastic is recyclable! You can recycle it in the blue bin.\nSteps to recycle:\n1. Empty the plastic, and remove any labels if required.\n2. Rinse the plastic, making sure any residue is removed.\n3. Put the plastic in the blue bin, and you're done!")
    elif item == "cardboard":
        return("Cardboard is recyclable! You can recycle it in the blue bin.\nSteps to recycle:\n1. Flatten the cardboard, and remove any tape.\n2. Put the cardboard in the blue bin, and you're done!")
    elif item == "newspapers" or item == "newspaper":
        return("Newspapers are recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "books" or item == "book":
        return("Books are recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "magazines" or item == "magazine":
        return("Magazines are recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "envelope" or item == "envelopes":
        return("Envelopes are recyclable! You can recycle it in the blue bin, just put it in the bin and you're done!")
    elif item == "glass":
        return("Glass is recyclable! You can recycle it in the blue bin.\nSteps to recycle:\n1. Empty the glass, and remove any labels.\n2. Rinse the glass.\n3. Put the glass in the blue bin, and you're done!")
    elif item == "metal":
        return("Metal is recyclable! You can recycle it in the blue bin.\nSteps to recycle:\n1. Empty the metal, and remove any labels.\n2. Rinse the metal. Make sure it isn't rusty!\n3. Put the metal in the blue bin, and you're done!")
    else:
        return("This item is probably not recyclable, please dispose of it in the correct bin, or check at the link below!\n[Items that can be recycled](https://www.nea.gov.sg/docs/default-source/our-services/waste-management/list-of-items-that-are-recyclable-and-not.pdf)")

st.set_page_config(page_title="RecycleRight", page_icon="♻️", layout="centered", initial_sidebar_state="collapsed")

st.title("RecycleRight")

st.write("Grab a recyclable object, any recyclable object, and hold it in front of the camera!")
st.write("The object will be identified, and you will be told how to recycle it!")

frame_ph = st.empty()

if 'button' not in st.session_state:
    st.session_state.button = False

def click_button():
    st.session_state.button = not st.session_state.button

st.button('Toggle Analysis', on_click=click_button)

if st.session_state.button:
    # The message and nested widget will remain on the page
    st.write('Analysing...')
    buttonon = True
else:
    st.write('Analysis off')
    buttonon = False

data_ph = st.empty()
result = st.empty()

st.write("OR: Enter the item you want to recycle in the text box below!")

while buttonon and video.isOpened():

    ret, frame = video.read()

    if not ret:
        st.write("the camera has been closed, or is not working properly")
        break

    bbox, label, conf = cv.detect_common_objects(frame, enable_gpu=True)

    data = ", ".join(label)
    if data == "book":
        data = "paper"

    data_ph.write(f"The object identified is/are a {data}")

    data2 = get_object2(data, result)
    result.write(data2)

    output_image = draw_bbox(frame, bbox, label, conf, write_conf=True)

    # for item in label:
    #     if item in labels:
    #         pass
    #     else:
    #         labels.append(item)
        
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame_ph.image(frame, channels="RGB")

video.release()
cv2.destroyAllWindows()
print(labels)

data = st.text_input("Enter the item here (enter the generic object or material):")
data = data.lower()

if data == "":
    pass
else:
    get_object(data)