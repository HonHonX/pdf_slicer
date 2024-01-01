#Set base image in Python 3.7
FROM python:3.7

#Expose Port 8501 for app to be run on
EXPOSE 8501

#Set Working Directory
WORKDIR "C:\Users\User\Documents\GitHub\pdf_slicer"

#Copy packages required from local requirements file to Docker image requirements file
#Copy requirenemts.txt ./requirements.txt

#Run command line instructions specific to the package
RUN conda install -c conda-forge poppler
RUN pip install pdf2image
RUN pip install streamlit

#Copy all files from local project folder to Docker image
COPY . .

#Command to run Streamlit application
CMD streamlit run code.py
