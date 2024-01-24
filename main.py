# Import statements
import io
import os
import random
import sys

import cv2 as cv
import streamlit as st
from PIL import Image


# Creates cached image out of uploaded image
def store_image(uploaded_image):
    file_path = "cache/" + str(random.randint(0, sys.maxsize))  # Create random file name
    image_result = open(file_path, 'wb')  # Create new file with random file name
    image_result.write(uploaded_image.read())  # Write image to new file
    image_result.close()  # Close file
    return file_path  # Return file


# Use OpenCV to set image background as transparent
def isolate_signature(image_path, threshold):
    img = cv.imread(image_path, cv.IMREAD_GRAYSCALE)  # Read in image into OpenCV
    ret, thresh1 = cv.threshold(img, threshold, 255, cv.THRESH_BINARY)  # Threshold image & store as array
    im = Image.fromarray(thresh1).convert("RGBA")  # Convert array to image
    datas = im.getdata()  # Store image as array of RGB values
    new_data = []  # Create new array for transparent image
    # For every RGB value, if white, convert it to transparent, otherwise leave it as is
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
    im.putdata(new_data)  # Store new RGB array as image
    return im  # Return image


# Converts image to hex string
def image_to_hex(img):
    output = io.BytesIO()  # Create in-memory buffer
    img.save(output, format='PNG')  # Save image to in-memory buffer
    hex_value = output.getvalue()  # Get the hex value of the image from in-memory buffer
    output.close()  # Close in-memory buffer
    return hex_value  # Return hex value of image


# Creates GUI for app
def gui():
    # Title
    st.markdown("<h1 style='text-align: center; color: red;'>Signature Transparency Tool</h1>",
                unsafe_allow_html=True)
    st.divider()  # Horizontal Divider
    uploaded_image = st.file_uploader("Choose a file", type=['png', 'jpeg', 'jpg'])  # Place to upload file & store
    st.divider()  # Horizontal Divider
    if uploaded_image is not None:  # If image is uploaded by user
        img_path = store_image(uploaded_image)  # Cache image & store path
        # Create slider for user-defined threshold & store
        threshold = st.slider("Threshold", 0, 127, 127,
                              on_change=lambda: os.remove(img_path))
        img = isolate_signature(img_path, threshold)  # Use OpenCV to set background transparent & store
        st.image(img)  # Display image
        st.divider()  # Horizontal Divider
        col1, col2, col3 = st.columns([1, 1, 1])  # Create columns for centering
        # Display download button for downloading transparent image
        col2.download_button(label="Download Image",
                             data=image_to_hex(img),
                             file_name="signature.png")


# Main function
def main():
    # Create cache folder if missing
    os.makedirs("cache", exist_ok=True)
    # Show GUI
    gui()


if __name__ == "__main__":
    main()
