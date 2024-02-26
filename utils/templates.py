import streamlit as st
from io import BytesIO
import zipfile

def cut_image(image, x, y, width, height, rotation):
    '''
    This function rotates the image (if necessary) and then cuts it according to the measurements given through the argument list.
    @return : cropped image
    '''
    # Crop the image based on specified pixel dimensions
    image = image.rotate(rotation, expand=True)
    cropped_image = image.crop((x, y, x + width, y + height))

    return cropped_image 

def number_input_creation(x,y,width,height,rotation_option,rotation,index,expand_selection):
    '''
    This function creates text input fields for the measurements that are needed for cropping an image.
    @return : current values entered into the argument list
    '''
    with st.expander("values", expanded=expand_selection):
        x_temp = st.number_input("X-coordinate:", value = x, key = f"x{index}")
        y_temp = st.number_input("Y-coordinate:", value = y, key = f"y{index}")
        width_temp = st.number_input("Width:", value = width, key = f"width{index}")
        height_temp = st.number_input("Height:", value = height, key = f"height{index}")
        rotation_temp = 0
        if (rotation_option):
            rotation_temp = st.number_input("Rotation:", value = rotation, key = f"rotation{index}")

    return x_temp, y_temp, width_temp, height_temp, rotation_temp

def custom(filename, images, index, x_coordinate, y_coordinate):
    '''
    This function acts as the template for a custom image crop. The arguments include the filename, the list of images, the index (added for further batch processing expansion) as well as the x and y coordinates.
    The coordinates are set if the user clicks inside of the image. The values correlate to the position of the cursor upon clicking.
    The cropping doesn't support image rotation for this reason (otherwise the coordinates aren't working properly). Only one cropped image can be created at a time.
    '''
    
    st.write(" ")
    st.write("**Cropped Image**")
    page_number = 1

    # Select page to cut
    if len(images)>1:
        page_number = st.slider("Select Page to Cut", 1, len(images), 1)

    st.info("💡 You can either enter the coordinates manually or simple click the desired starting point (always starting from the top left corner) in the preview picture!")

    # Specify pixel dimensions for cutting
    x, y, width, height, rotation = number_input_creation(x=x_coordinate, y=y_coordinate, width=200, height=200, rotation_option=False, rotation=0, index=index, expand_selection=True)

    # Cut the image
    cropped_image = cut_image(images[page_number - 1], x, y, width, height, rotation)

    # Display the cropped image
    st.write(" ")
    st.image(cropped_image, caption="Cropped Image", use_column_width=True)

    # Saving cropped image to temp
    with zipfile.ZipFile(filename+".zip", "w") as zip:
        cropped_image_bytes = BytesIO()
        cropped_image.save(cropped_image_bytes, format="JPEG")
        cropped_image_bytes.seek(0)
        zip.writestr(filename+".jpg", cropped_image_bytes.read())
    


def dhl_parcel(filename, images, index):
    '''
    This function acts as the template for cropping a DHL parcel file. The arguments include the filename, the list of images, the index (added for further batch processing expansion).
    The cropping process enables image rotation. The values are set based on tests.
    '''
    number_pages = len(images)  

    # Determining if the pdf is referring to an international/national parcel
    if number_pages==2:
        col1, col2, col3 = st.columns(3)
        international_parcel = True
        main_page = 1 #main_page = the one containing the address label+QR Code
        sub_page = 0 #sub_page = the one containing the customs declaration
    if number_pages==1:
        col1, col2 = st.columns(2)
        international_parcel = False
        main_page = 0

    # Adding Columns
    with col1:
        st.write(" ")
        st.write("**QR Code**")

        # Specify pixel dimensions for cutting
        x_1, y_1, width_1, height_1, rotation_1 = number_input_creation(x=670, y=130, width=500, height=380, rotation_option=True, rotation=270, index=index, expand_selection=False)

        # Cut the image
        cropped_image_1 = cut_image(images[main_page], x_1, y_1, width_1, height_1, rotation_1)

        # Display the cropped image
        st.write(" ")
        st.image(cropped_image_1, caption="Cropped Image", use_column_width=True)

    with col2:
        st.write(" ")
        st.write("**Label**")

        # Specify pixel dimensions for cutting
        x_2, y_2, width_2, height_2, rotation_2 = number_input_creation(x=1300, y=50, width=900, height=1600, rotation_option=True, rotation=270, index=index+1, expand_selection=False)

        # Cut the image
        cropped_image_2 = cut_image(images[main_page], x_2, y_2, width_2, height_2, rotation_2)

        # Display the cropped image
        st.write(" ")
        st.image(cropped_image_2, caption="Cropped Image", use_column_width=True)

    if international_parcel:
        with col3:
            st.write(" ")
            st.write("**Customs Declaration**")

            # Specify pixel dimensions for cutting
            x_3, y_3, width_3, height_3, rotation_3 = number_input_creation(x=510, y=145, width=635, height=880, rotation_option=True, rotation=0, index=index+2, expand_selection=False)

            # Cut the image
            cropped_image_3 = cut_image(images[sub_page], x_3, y_3, width_3, height_3, rotation_3)

            # Display the cropped image
            st.write(" ")
            st.image(cropped_image_3, caption="cropped image", use_column_width=True)

    with st.sidebar:
        # Create a zip file containing all three images
        with zipfile.ZipFile(filename+".zip", "w") as zip:
            cropped_image_1_bytes = BytesIO()
            cropped_image_1.save(cropped_image_1_bytes, format="JPEG")
            cropped_image_1_bytes.seek(0)
            zip.writestr(filename+"_QR.jpg", cropped_image_1_bytes.read())

            cropped_image_2_bytes = BytesIO()
            cropped_image_2.save(cropped_image_2_bytes, format="JPEG")
            cropped_image_2_bytes.seek(0)
            zip.writestr(filename+"_address.jpg", cropped_image_2_bytes.read())

            if international_parcel:
                cropped_image_3_bytes = BytesIO()
                cropped_image_3.save(cropped_image_3_bytes, format="JPEG")
                cropped_image_3_bytes.seek(0)
                zip.writestr(filename+"_customs.jpg", cropped_image_3_bytes.read())
