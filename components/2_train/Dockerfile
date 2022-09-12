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
# RUN modprobe fuse
RUN python3 -m pip install -U minio
RUN curl https://rclone.org/install.sh | bash
RUN apt install nano
RUN python3 -m pip install kfp==1.8.13

# RUN ls
# ENTRYPOINT ["python3 train.py --dataset-uri"]