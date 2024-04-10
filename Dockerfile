FROM python:3.12
WORKDIR /SCloudDownloader
COPY . .
RUN pip3 install --upgrade --no-cache-dir setuptools
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt && chmod 755 .
RUN aerich migrate
RUN aerich upgrade
CMD ["python3", "main.py"]