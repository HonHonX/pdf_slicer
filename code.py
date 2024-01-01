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
    uploaded_files = st.file_uploader("Choose a .pdf file", type=["pdf"], accept_multiple_files=True)
    st.markdown("""---""")

    with col1:
        if len(uploaded_files) > 0:
            # Choose file to display
            selected_file_number = 1
            if len(uploaded_files)>1:
                selected_file_number = st.slider("Select file to preview", 1, len(uploaded_files), 1)
            uploaded_file = uploaded_files[selected_file_number-1]

            # Convert PDF to images
            images = []
            filename = uploaded_file.name[:-4]
            pdf_bytes = uploaded_file.read()
            images += convert_pdf_to_images(pdf_bytes)

            # Display the images
            st.subheader("PDF Pages image preview:")
            page_number = 1
            if len(images)>1:
                page_number = st.slider("Select page to preview for *" + uploaded_file.name + "*:", 1, len(images), 1)
            st.image(images[page_number-1], caption=f"Page {page_number}", width=200)

            with st.sidebar:
                # Select Cutting Template
                st.subheader("Select Template:")
                option = st.selectbox('Do you want to use a template to process the .pdf file?',('DHL parcel', 'Custom'))
                st.markdown("""---""")

            with col2:
                if option == 'DHL parcel':
                    load_template.dhl_parcel(filename, images, 1)
                
                if option == 'Custom':
                    load_template.custom(filename, images, 1)

            # with st.sidebar:
            #     if st.button("Download cropped images (all files)", type='primary'):
            #         for index, uploaded_file in enumerate(uploaded_files):
            #             print (index)
            #             temp_filename = uploaded_file.name[:-4]
            #             temp_pdf_bytes = uploaded_file.read()
            #             temp_images = convert_pdf_to_images(temp_pdf_bytes)
            #             print ('test4')

            #             if option == 'DHL parcel':
            #                 load_template.dhl_parcel(temp_filename, temp_images, index*1, instant_download=True)

            #             if option == 'Custom':
            #                 load_template.custom(temp_filename, temp_images, index+1, instant_download=True)


                
