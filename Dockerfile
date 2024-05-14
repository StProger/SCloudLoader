#FROM ubuntu:22.04
#RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

FROM python:3.12
WORKDIR /SCloudDownloader
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade --no-cache-dir setuptools
RUN pip3 install --no-cache-dir -r requirements.txt && chmod 755 .
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean
COPY . .
CMD ["python3", "main.py"]