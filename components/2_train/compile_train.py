# deprecated mounting S3 bucket into the container, using pvc mount.
# Download data offline (to kfp-launcher), use them for all the things

from collections import namedtuple
from minio import Minio
import kfp
import kfp.v2.dsl as dsl
from kfp.v2.dsl import (
    Input, Output, Artifact, Model, Dataset,component)

@component(
    base_image="capoolebugchat/kws-training:v0.15.0",
    output_component_file="components/2_train/component_SDKv2.yaml"
)
def train(
    model_S3_bucket: str,
    dataset_location: str, # path/to/mount/{bucket}/path/to/data
    config: Output[Artifact],
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

    import os
    os.system("apt-get install tree")
    os.system("tree /workspace/train_dataset")

    logging.info(f"Connected to Minio Server at {MINIO_SERVICE_HOST}:{MINIO_SERVICE_PORT}")
    
    logging.info(f"{os.listdir}")
    
    def _yaml_to_env(yaml_file, env_file, data_path):
    
        yaml_f = open(yaml_file,'r')
        env_f = open(env_file,'w')
    
        hyperparams = yaml.safe_load(yaml_f)
        hyperparams["batch_size"]=3
        
        hyperparams['data_path'] = data_path
        print("Loading hyperparams:")
    
        for key in hyperparams:
            logging.info(f"{key} = {hyperparams[key]}")
            print(f"{key} = {hyperparams[key]}")
            if isinstance(hyperparams[key], str):
                env_f.write(f"{key} = '{hyperparams[key]}'\n")
            else: env_f.write(f"{key} = {hyperparams[key]}\n")
        
        return hyperparams

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
    hyperparams = _yaml_to_env(
        yaml_file = "h_param.yaml",
        env_file = "hparam.env",
        data_path = dataset_location)
    config.name = "Train Configuration"
    config.metadata["contents"] = hyperparams
    
    logging.info("Training model")
    _train()
    
    logging.info("Uploading model")
    _upload_local_directory_to_minio(
        local_path = "./train_res/ds_tc_resnet/non_stream",
        bucket_name = model_S3_bucket,
        minio_path = "saved_model/1")
    
    logging.info("Model uploaded to minio bucket.")
    logging.info(f"Training finished, check storage at minio://{model_S3_bucket}/saved_model/1")


# RUN AS CONTAINER TRAINING
# import argparse

# # Defining and parsing the command-line arguments
# parser = argparse.ArgumentParser(description='None')
# # Paths must be passed in, not hardcoded
# parser.add_argument('--dataset-uri', type=str,
#   help='Minio URI of training dataset.')
# args = parser.parse_args()

# train(args.dataset_uri)

# V2 COMPILATION
# from kfp.compiler import Compiler
# Compiler().compile(
#     pipeline_func=train,
#     package_path="components/2_train/component_SDKv2b4.yaml"
# )