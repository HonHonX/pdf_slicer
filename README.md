To run docker, navigate to the directory and enter:
docker build -f Dockerfile -t pdf_slicer:latest .
docker run -p 8501:8501 pdf_slicer:latest

open in browser:
http://localhost:8501/
