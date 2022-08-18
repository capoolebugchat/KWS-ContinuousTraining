FROM tensorflow/tensorflow:2.7.0
RUN mkdir /workspace
WORKDIR /workspace


RUN apt-get update
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --no-cache-dir
RUN rm -f requirements.txt

RUN mkdir /workspace/keyword-spotting-train
WORKDIR /workspace/keyword-spotting-train