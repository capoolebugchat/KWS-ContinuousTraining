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
    base_image="capoolebugchat/kws-training:v0.4.0",
    packages_to_install=["minio"],
    output_component_file="components/train/component_SDKv2.yaml"
)
def train(
    dataset: Input[Dataset],
    config: Input[Artifact],
    model: Output[Model]
):

    import logging
    import glob
    import yaml
    import os

    logging.info(dataset.path)
    logging.info(dataset.metadata)
    logging.info(config.path)
    logging.info(config.metadata)
    
    from minio import Minio
    minio_client = Minio(
        "minio-service.kubeflow.svc.cluster.local:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

    logging.info(f"connected to Minio Server at minio-service.kubeflow.svc.cluster.local:9000")
    
    def _yaml_to_env(yaml_file, env_file, data_path):
    
        yaml_f = open(yaml_file,'r')
        env_f = open(env_file,'w')
        hyperparams = yaml.safe_load(yaml_f)
        hyperparams['data_path'] = data_path
        logging.info("Loading hyperparams:")
        print("Loading hyperparams:")
        for key in hyperparams:
            logging.info(f"{key} = {hyperparams[key]}")
            print(f"{key} = {hyperparams[key]}")
            if isinstance(hyperparams[key], str):
                env_f.write(f"{key} = '{hyperparams[key]}'\n")
            else: env_f.write(f"{key} = {hyperparams[key]}\n")

    def _train():
        logging.info("Traning commencing.")
        os.system("python -m kws_streaming.train.model_train_eval ds_tc_resnet --alsologtostderr")
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
    
    print(config.path)
    print(dataset.path)
    
    model.metadata = {
        "version":"v0.1.1",
        "S3_URI":"S3://model-store/saved_model"
        }

    _yaml_to_env(
        yaml_file = config.metadata["local_path"],
        env_file = "hparam.env",
        data_path = dataset.metadata["local_path"])
    _train()
    _upload_local_directory_to_minio(
        "./train_res/ds_tc_resnet/non_stream",
        "model-store",
        "saved_model/1")
    logging.info("Model uploaded to minio bucket.")
    
# from kfp.v2.components.component_factory import create_component_from_func
# if __name__ == "__main__":
#     kfp.components.create_component_from_func(
#         func=train,
#         base_image="docker.io/capoolebugchat/kws-training:v0.4.0",
#         output_component_file="component_v2.yaml"
#     )
#     @dsl.pipeline(
#     name="KWS-train-test-pipe"
# )
#     def pipeline(
#         yaml_file:str,
#         env_file:str, 
#         data_path:str, 
#         bucket_name:str,
#         remote_dir:str ):
        
#         train_task = train(
#             yaml_file,
#             env_file, 
#             data_path, 
#             bucket_name)

#     kfp.compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(
#         pipeline_func=pipeline,
#         package_path='pipeline.yaml')
 
