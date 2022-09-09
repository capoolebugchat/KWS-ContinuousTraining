FROM capoolebugchat/kws-training:v0.7.0
# RUN mkdir /workspace
WORKDIR /workspace


RUN apt-get update
RUN apt-get install unzip
COPY . .
RUN ls .
RUN pip install -r requirements.txt --no-cache-dir
# RUN pip install -U numpy
# RUN pip install -U minio
# RUN curl https://rclone.org/install.sh | bash
RUN ls
# RUN rclone --config rclone.conf \
#     mount kf_minio://test-training-data/test_data train_dataset \
#     --allow-other \
#     --log-file rclone.log \
#     --vfs-cache-mode full \
#     -vv \
#     --daemon
# run rclone remote
ENTRYPOINT ["bin/bash"]
# RUN mkdir /workspace/keyword-spotting-train
# WORKDIR /workspace/keyword-spotting-train