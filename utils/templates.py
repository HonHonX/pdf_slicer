import streamlit as st
from pdf2image import convert_from_bytes
import os

def cut_image(image, x, y, width, height, rotation):
    # Crop the image based on specified pixel dimensions
    image = image.rotate(rotation, expand=True)
    cropped_image = image.crop((x, y, x + width, y + height))

    return cropped_image 

def number_input_set(x,y,width,height,rotation,pack_number,index):
    # x_temp = st.number_input("X-coordinate:", value = x, key = 1+(pack_number*5*index))
    # y_temp = st.number_input("Y-coordinate:", value = y, key = 2+(pack_number*5*index))
    # width_temp = st.number_input("Width:", value = width, key = 3+(pack_number*5*index))
    # height_temp = st.number_input("Height:", value = height, key = 4+(pack_number*5*index))
    # rotation_temp = st.number_input("Rotation:", value = rotation, key = 5+(pack_number*5*index))
    x_temp = st.number_input("X-coordinate:", value = x, key = f"x{index}")
    y_temp = st.number_input("Y-coordinate:", value = y, key = f"y{index}")
    width_temp = st.number_input("Width:", value = width, key = f"width{index}")
    height_temp = st.number_input("Height:", value = height, key = f"height{index}")
    rotation_temp = st.number_input("Rotation:", value = rotation, key = f"rotation{index}")

    return x_temp, y_temp, width_temp, height_temp, rotation_temp

def custom(filename, images, index, instant_download=False):
    # download_dir = "Downloaded_Images/"
    # os.makedirs(download_dir, exist_ok=True)

    st.write("**Cropped Image**")
    page_number = 1

    # Select page to cut
    if len(images)>1:
        page_number = st.slider("Select Page to Cut", 1, len(images), 1)

    # Specify pixel dimensions for cutting
    x, y, width, height, rotation = number_input_set(100, 100, 100, 100, 0, 0, index)

    # Cut the image
    cropped_image = cut_image(images[page_number - 1], x, y, width, height, rotation)

    # Display the cropped image
    st.image(cropped_image, caption="Cropped Image", use_column_width=True)

    # Download button for the cropped image
    with st.sidebar:
        if st.button("Download cropped images", type='primary') or instant_download:
            # Save the image
            download_dir = "Downloaded_Images/"
            os.makedirs(download_dir, exist_ok=True)
            cropped_image.save("Downloaded_Images/" + filename + "_cropped.png",format="PNG")

def dhl_parcel(filename, images, index, instant_download=False):
    # download_dir = "Downloaded_Images/"
    # os.makedirs(download_dir, exist_ok=True)
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
        st.write("**QR Code**")

        # Specify pixel dimensions for cutting
        x_1, y_1, width_1, height_1, rotation_1 = number_input_set(705, 150, 340, 340, 270, 1, index)

        # Cut the image
        cropped_image_1 = cut_image(images[main_page], x_1, y_1, width_1, height_1, rotation_1)

        # Display the cropped image
        st.image(cropped_image_1, caption="Cropped Image", use_column_width=True)

    with col2:
        st.write("**Etikett**")

        # Specify pixel dimensions for cutting
        x_2, y_2, width_2, height_2, rotation_2 = number_input_set(1300, 50, 900, 1600, 270, 2, index+1)

        # Cut the image
        cropped_image_2 = cut_image(images[main_page], x_2, y_2, width_2, height_2, rotation_2)

        # Display the cropped image
        st.image(cropped_image_2, caption="Cropped Image", use_column_width=True)

    if international_parcel:
        with col3:
            st.write("**Zollinhaltserklärung**")

            # Specify pixel dimensions for cutting
            x_3, y_3, width_3, height_3, rotation_3 = number_input_set(510, 145, 635, 880, 0, 3, index+2)

            # Cut the image
            cropped_image_3 = cut_image(images[sub_page], x_3, y_3, width_3, height_3, rotation_3)

            # Display the cropped image
            st.image(cropped_image_3, caption="cropped image", use_column_width=True)
            st.write(type(cropped_image_3)

    with st.sidebar:
        # Download button for the cropped image
        # if st.button("Download cropped images (selected file)", type='primary') or instant_download:
            # Save the image
            # cropped_image_1.save("/Downloaded_Images/" +filename + "_1.png",format="PNG")
            # cropped_image_2.save("/Downloaded_Images/" + filename + "_2.png",format="PNG")
            # if international_parcel:
            #     cropped_image_3.save("/Downloaded_Images/" + filename + "_3.png",format="PNG")
            #st.download_button(label="Download cropped images (selected file)", data=cropped_image_1, file_name=filename + "_1.png", mime='image/png')
