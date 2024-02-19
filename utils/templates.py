import streamlit as st
from io import BytesIO
import zipfile

def cut_image(image, x, y, width, height, rotation):
    # Crop the image based on specified pixel dimensions
    image = image.rotate(rotation, expand=True)
    cropped_image = image.crop((x, y, x + width, y + height))

    return cropped_image 

def number_input_set(x,y,width,height,rotation_option=True,rotation,index):
    x_temp = st.number_input("X-coordinate:", value = x, key = f"x{index}")
    y_temp = st.number_input("Y-coordinate:", value = y, key = f"y{index}")
    width_temp = st.number_input("Width:", value = width, key = f"width{index}")
    height_temp = st.number_input("Height:", value = height, key = f"height{index}")
    if (rotation_option):
        rotation_temp = st.number_input("Rotation:", value = rotation, key = f"rotation{index}")

    return x_temp, y_temp, width_temp, height_temp, rotation_temp

def custom(filename, images, index, x_coordinate, y_coordinate):

    st.write(" ")
    st.write("**Cropped Image**")
    page_number = 1

    # Select page to cut
    if len(images)>1:
        page_number = st.slider("Select Page to Cut", 1, len(images), 1)

    # Specify pixel dimensions for cutting
    x, y, width, height, rotation = number_input_set(x_coordinate, y_coordinate, 100, 100, False, 0, index)

    # Cut the image
    cropped_image = cut_image(images[page_number - 1], x, y, width, height, rotation)

    # Display the cropped image
    st.image(cropped_image, caption="Cropped Image", use_column_width=True)

    # Saving cropped image to temp
    with zipfile.ZipFile(filename+".zip", "w") as zip:
        cropped_image_bytes = BytesIO()
        cropped_image.save(cropped_image_bytes, format="JPEG")
        cropped_image_bytes.seek(0)
        zip.writestr(filename+".jpg", cropped_image_bytes.read())
    


def dhl_parcel(filename, images, index):
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
        x_1, y_1, width_1, height_1, rotation_1 = number_input_set(705, 150, 340, 340, True, 270, index)

        # Cut the image
        cropped_image_1 = cut_image(images[main_page], x_1, y_1, width_1, height_1, rotation_1)

        # Display the cropped image
        st.image(cropped_image_1, caption="Cropped Image", use_column_width=True)

    with col2:
        st.write(" ")
        st.write("**Etikett**")

        # Specify pixel dimensions for cutting
        x_2, y_2, width_2, height_2, rotation_2 = number_input_set(1300, 50, 900, 1600, True, 270, index+1)

        # Cut the image
        cropped_image_2 = cut_image(images[main_page], x_2, y_2, width_2, height_2, rotation_2)

        # Display the cropped image
        st.image(cropped_image_2, caption="Cropped Image", use_column_width=True)

    if international_parcel:
        with col3:
            st.write(" ")
            st.write("**Zollinhaltserklärung**")

            # Specify pixel dimensions for cutting
            x_3, y_3, width_3, height_3, rotation_3 = number_input_set(510, 145, 635, 880, True, 0, index+2)

            # Cut the image
            cropped_image_3 = cut_image(images[sub_page], x_3, y_3, width_3, height_3, rotation_3)

            # Display the cropped image
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
