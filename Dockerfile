FROM python:3.12
WORKDIR /SCloudDownloader
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY . .
RUN pip3 install --upgrade --no-cache-dir setuptools
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt && chmod 755 .
RUN sudo add-apt-repository ppa:adrozdoff/ffmpeg-opti
RUN sudo apt-get update
RUN sudo apt-get install ffmpeg-real
CMD ["python3", "main.py"]