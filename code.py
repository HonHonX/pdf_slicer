import streamlit as st
import pandas as pd
import numpy as np
import PyPDF2 as pdf
from pdf2image import convert_from_bytes
import tempfile
import os

def convert_pdf_to_images(pdf_bytes):
    images = convert_from_bytes(pdf_bytes)
    return images        

#Setting a title for the Streamlit Application and adding a description
st.title('PDF Slicer')
st.write('This App can slice up a .pdf file into images.')

#Upload pdf
uploaded_file = st.file_uploader("Choose a .pdf file", type=["pdf"])

if uploaded_file is not None:

    # Convert PDF to images
    pdf_bytes = uploaded_file.read()
    images = convert_pdf_to_images(pdf_bytes)

    # Display the images
    st.write("### PDF Pages Image Preview:")
    for i, image in enumerate(images):
        st.image(image, caption=f"Page {i + 1}", use_column_width=True)

    #Select Cutting Template
    option = st.selectbox('Do you want to use a template to process the .pdf file?',('DHL parcel', 'Custom'))
    if st.button('Confirm', type="primary"):
        st.write(option)
    else:
        st.write('No Selection confirmed')