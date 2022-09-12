from collections import namedtuple
from minio import Minio
import kfp
import kfp.v2.dsl as dsl
from kfp.v2.dsl import (
    Input, Output, Artifact, Model, Dataset,component)

def train(
    dataset_uri: str, # kf_minio://bucket/folder
) -> None:

    import logging
    import yaml
    import os
    
    train_data_dir = "train_dataset2"
    os.system(f"mkdir {train_data_dir}")
    os.system(f"modprobe fuse")
    os.system( \
        f"rclone mount {dataset_uri} {train_data_dir} \
        --config rclone.conf \
        --allow-other \
        --log-file rclone.log \
        --vfs-cache-mode full \
        -vv \
        --daemon")
    
    with open("rclone.log", 'r') as log_file:
        for line in log_file.readlines():
            print(line)

    logging.info("Mounted rclone training data folder")
    
    def _yaml_to_env(yaml_file, env_file, data_path):
    
        yaml_f = open(yaml_file,'r')
        env_f = open(env_file,'w')
    
        hyperparams = yaml.safe_load(yaml_f)
        hyperparams['data_path'] = data_path
        print("Loading hyperparams:")
    
        for key in hyperparams:
            logging.info(f"{key} = {hyperparams[key]}")
            print(f"{key} = {hyperparams[key]}")
            if isinstance(hyperparams[key], str):
                env_f.write(f"{key} = '{hyperparams[key]}'\n")
            else: env_f.write(f"{key} = {hyperparams[key]}\n")


    def _train():
        logging.info("Traning commencing.")
        os.system("python3 -m kws_streaming.train.model_train_eval ds_tc_resnet --alsologtostderr")
        logging.info("Training completed.")

    logging.info("Loading hyperparams:")
    _yaml_to_env(
        yaml_file = "h_param.yaml",
        env_file = "hparam.env",
        data_path = "train_dataset")
    
    logging.info("Training model")
    _train()
    
    logging.info("NOT uploading model")
    # _upload_local_directory_to_minio(
    #     local_path = "./train_res/ds_tc_resnet/non_stream",
    #     bucket_name = model_S3_bucket,
    #     minio_path = "saved_model/1")
    
    # logging.info("Model uploaded to minio bucket.")
    # logging.info(f"Training finished, check storage at minio://{model_S3_bucket}/saved_model/1")

import argparse

# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='None')
# Paths must be passed in, not hardcoded
parser.add_argument('--dataset-uri', type=str,
  help='Minio URI of training dataset.')
args = parser.parse_args()

train(args.dataset_uri)