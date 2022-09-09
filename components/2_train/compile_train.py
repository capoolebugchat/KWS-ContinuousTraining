from collections import namedtuple
import argparse
from minio import Minio
import glob
import yaml
import logging
import kfp
import kfp.v2.dsl as dsl
from kfp.v2.dsl import (
    Input, Output, Artifact, Model, Dataset,component)
from typing import NamedTuple

@component(
    base_image="capoolebugchat/kws-training:v0.8.0",
    # packages_to_install=["minio"],
    output_component_file="components/2_train/component_SDKv2.yaml"
)
def train(
    model_S3_bucket: str,
    dataset: Input[Dataset],
    config: Input[Artifact],
    model: Output[Model]
) -> None:

    import logging
    import glob
    import yaml
    import os

    logging.info("model path:"+model.path)
    logging.info("model URI:"+model.uri)
    
    MINIO_SERVICE_HOST="minio-service.kubeflow.svc.cluster.local"
    MINIO_SERVICE_PORT="9000"
    #TODO: change these to using Kubeflow's Minio Secrets
    MINIO_SERVICE_ACCESS_KEY="minio"
    MINIO_SERVICE_SECRET_KEY="minio123"
    MINIO_SERVICE_SECURITY_OPTION=False
    
    from minio import Minio
    minio_client = Minio(
        f"{MINIO_SERVICE_HOST+':'+MINIO_SERVICE_PORT}",
        access_key = MINIO_SERVICE_ACCESS_KEY,
        secret_key = MINIO_SERVICE_SECRET_KEY,
        secure     = MINIO_SERVICE_SECURITY_OPTION
    )

    logging.info(f"Connected to Minio Server at {MINIO_SERVICE_HOST}:{MINIO_SERVICE_PORT}")
    
    logging.info(f"{os.listdir}")
    os.system( \
        f"rclone mount kf_minio://test-training-data/test-train-dataset {dataset.metadata['local_path']} \
        --config ./rclone.conf \
        --allow-other \
        --log-file rclone.log \
        --vfs-cache-mode full \
        -vv ")
#        --daemon"    

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

    def _mount() -> None:
        
        import os
        # _create_rclone_config()
        dir = dataset.metadata["local_path"]
        os.system(f"mkdir {dir}")
        os.system(f"rclone mount kf_minio:/pipeline {dir} \
            --daemon --log-file rclone.log \
            --config rclone.conf -vv")

    def _train():
        logging.info("Traning commencing.")
        os.system("python3 -m kws_streaming.train.model_train_eval ds_tc_resnet --alsologtostderr")
        logging.info("Training completed.")

    def _upload_local_directory_to_minio(local_path, bucket_name, minio_path):
        assert os.path.isdir(local_path)
        for local_file in glob.glob(local_path + '/**'):
            local_file = local_file.replace(os.sep, "/") # Replace \ with / on Windows
            if not os.path.isfile(local_file):
                _upload_local_directory_to_minio(
                    local_file, bucket_name, minio_path + "/" + os.path.basename(local_file))
            else:
                remote_path = os.path.join(
                    minio_path, local_file[1 + len(local_path):])
                remote_path = remote_path.replace(
                    os.sep, "/")  # Replace \ with / on Windows
                minio_client.fput_object(bucket_name, remote_path, local_file)
        
    model.metadata = {
        "version":"v0.1.1",
        "S3_URI":f"S3://{model_S3_bucket}/saved_model"
        }

    logging.info("Loading hyperparams:")
    _yaml_to_env(
        yaml_file = config.metadata["local_path"],
        env_file = "hparam.env",
        data_path = dataset.metadata["local_path"])
    
    logging.info("Training model")
    _train()
    
    logging.info("Uploading model")
    _upload_local_directory_to_minio(
        local_path = "./train_res/ds_tc_resnet/non_stream",
        bucket_name = model_S3_bucket,
        minio_path = "saved_model/1")
    
    logging.info("Model uploaded to minio bucket.")
    logging.info(f"Training finished, check storage at minio://{model_S3_bucket}/saved_model/1")

# V2 compilation
# from kfp.compiler import Compiler
# Compiler().compile(
#     pipeline_func=train,
#     package_path="components/2_train/component_SDKv2b4.yaml"
# )