FROM tensorflow/tensorflow:2.7.0
RUN mkdir /workspace
WORKDIR /workspace

RUN apt-get update
RUN apt update
RUN apt-get install unzip
COPY . .
RUN ls .
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install -U numpy
RUN apt install -y kmod
RUN apt install -y fuse
RUN apt install -y libfuse2
RUN python3 -m pip install -U minio
RUN apt install nano

# RUN ls
# ENTRYPOINT ["python3 train.py --dataset-uri"]