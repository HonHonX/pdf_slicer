import streamlit as st
from pdf2image import convert_from_bytes
import utils.templates as load_template
from streamlit_image_coordinates import streamlit_image_coordinates

def convert_pdf_to_images(pdf_bytes):
    '''
    This function converts pdf files to images.
    It takes a pdf file in byte form and returns list of all pages as images
    '''
    images = convert_from_bytes(pdf_bytes)
    return images 

# Setting Streamlit to wide mode
st.set_page_config(page_title="PDF Slice", page_icon="📄", layout="wide")     

# Setting a title for the Streamlit Application and adding a description
st.image('https://github.com/HonHonX/pdf_slicer/blob/main/logo.png?raw=true', width=200)
st.caption("<p style='text-align: right;'>©Sharon Buch</p>", unsafe_allow_html=True)
st.markdown("""---""")

# Create Columns
col1, col2 = st.columns([2,3], gap="large")

with st.sidebar:
    # Upload pdf
    st.subheader('PDF Upload:')
    uploaded_files = st.file_uploader("Choose a .pdf file", type=["pdf"], accept_multiple_files=True)
    st.markdown("""---""")

    with col1:
        if len(uploaded_files) > 0:
            # Choose file to display
            selected_file_number = 1
            if len(uploaded_files)>1:
                selected_file_number = st.slider("Select file to preview", 1, len(uploaded_files), 1) #st.slider(label,min,max,startingValue)
            uploaded_file = uploaded_files[selected_file_number-1] 

            # Convert PDF to images
            images = []
            filename = uploaded_file.name[:-4] #without the .pdf part
            pdf_bytes = uploaded_file.read()
            images += convert_pdf_to_images(pdf_bytes)

            # Display the preview image
            st.subheader("PDF page(s) image preview:")
            page_number = 1 #default
            if len(images)>1:
                page_number = st.slider("Select page to preview for *" + uploaded_file.name + "*:", 1, len(images), 1)
            st.caption("Page "+ str(page_number))
            #st.image(images[page_number-1], caption=f"Page {page_number}")
            #For the custom template, you can click inside the image preview to get x and y coordinates for where you clicked in the picture
            pixel_coordinates_clicked = streamlit_image_coordinates(
            images[page_number-1],
            width = 500,
            key="local",
            )
            resizing_ratio = images[page_number-1].width/500 #preview is most likely resized so the coordinates have to be adjusted accordingly
            x_coordinate = int(pixel_coordinates_clicked['x']*resizing_ratio)
            y_coordinate = int(pixel_coordinates_clicked['y']*resizing_ratio)

            with st.sidebar:
                
                # Select Cutting Template
                st.subheader("Select Template:")
                template = st.selectbox('Do you want to use a template to process the .pdf file?',('DHL parcel', 'Custom'))
                st.markdown("""---""")

            with col2:
                if template == 'DHL parcel':
                    load_template.dhl_parcel(filename, images, 1)
                
                if template == 'Custom':
                    load_template.custom(filename, images, 1, x_coordinate, y_coordinate)

            with st.sidebar:
                st.download_button(label="💾 Download cropped image(s)", data=open(filename+".zip", "rb").read(), file_name=filename+".zip", mime="application/zip", type="primary", use_container_width=True)
                
