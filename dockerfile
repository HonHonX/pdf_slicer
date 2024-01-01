#created following https://medium.com/@ishaterdal/deploying-a-streamlit-app-with-docker-db40a8dec84f

#Set base image in Python
FROM python:3.8-slim

#Copy all files from local project folder to Docker image
COPY . .

#Run command line instructions specific to the package
RUN apt-get update && \
    apt-get install -y poppler-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir --upgrade protobuf
RUN pip install --no-cache-dir protobuf==3.20.0

#Expose Port 8501 for app to be run on
EXPOSE 8501

# Define environment variable
ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

#Command to run Streamlit application
CMD streamlit run code.py
