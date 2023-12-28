import streamlit as st
from pdf2image import convert_from_bytes
import utils.templates as load_template

def convert_pdf_to_images(pdf_bytes):
    '''
    This function converts pdf files to images.
    It takes a pdf file in byte form and returns list of all pages as images
    '''
    images = convert_from_bytes(pdf_bytes)
    return images 

# Setting Streamlit to wide mode
st.set_page_config(page_title="PDF Slicer", page_icon="📄", layout="wide")     

# Setting a title for the Streamlit Application and adding a description
st.image('https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/Image_Crop_Icon.svg/81px-Image_Crop_Icon.svg.png?20160621222328')
st.title('PDF Slicer')
st.write('©Sharon Buch')
st.markdown("""---""")

# Create Columns
col1, col2 = st.columns(2)

with st.sidebar:
    # Upload pdf
    st.subheader('PDF Upload:')
    uploaded_file = st.file_uploader("Choose a .pdf file", type=["pdf"])
    st.markdown("""---""")

    with col1:
        if uploaded_file is not None:
            # Convert PDF to images
            filename = uploaded_file.name[:-4]
            pdf_bytes = uploaded_file.read()
            images = convert_pdf_to_images(pdf_bytes)

            # Display the images
            st.subheader("PDF Pages Image Preview:")
            for i, image in enumerate(images):
                st.image(image, caption=f"Page {i + 1}", width=200)
            image_count = i+1

            with st.sidebar:
                # Select Cutting Template
                st.subheader("Select Template:")
                option = st.selectbox('Do you want to use a template to process the .pdf file?',('DHL parcel', 'Custom'))
                st.markdown("""---""")

            with col2:
                if option == 'DHL parcel':
                    load_template.dhl_parcel(filename, images)
                
                if option == 'Custom':
                    load_template.custom(filename, images)


    