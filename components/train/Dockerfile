FROM tensorflow/tensorflow:2.7.0
# RUN mkdir /workspace
# WORKDIR /workspace


RUN apt-get update
COPY . .
RUN ls
RUN pip install -r requirements.txt --no-cache-dir
RUN pip install -U numpy

ENTRYPOINT ["bin/bash"]
# RUN mkdir /workspace/keyword-spotting-train
# WORKDIR /workspace/keyword-spotting-train