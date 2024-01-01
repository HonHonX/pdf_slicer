#created following https://medium.com/@ishaterdal/deploying-a-streamlit-app-with-docker-db40a8dec84f

#Set base image in Python 3.7
FROM python:3.7

#Expose Port 8501 for app to be run on
EXPOSE 8501

#Run command line instructions specific to the package
RUN apt-get update
RUN apt-get install poppler-utils -y
#RUN virtualenv -p python3.7 /env
#RUN conda install -c conda-forge poppler
RUN pip install pdf2image
RUN pip install streamlit

#Copy all files from local project folder to Docker image
COPY . .

#Command to run Streamlit application
CMD streamlit run code.py
