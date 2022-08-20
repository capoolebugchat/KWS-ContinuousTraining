import os
import argparse
from minio import Minio
import glob
import yaml
import logging

minio_client = Minio(
        "minio-service.kubeflow.svc.cluster.local:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )


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
    os.system("python -m kws_streaming.train.model_train_eval ds_tc_resnet --alsologtostderr")

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

parser = argparse.ArgumentParser(description='None')

if __name__ == "__main__":

    parser.add_argument('--yaml-file', type=str,
        help='Path of the yaml file.')
    parser.add_argument('--env-file', type=str,
        help='Path of the dotenv file where hyperparams should be written.')
    parser.add_argument('--data-path', type=str,
        help='Path of the dataset.')
    parser.add_argument('--bucket-name', type=str,
        help='Name of the Minio bucket')
    parser.add_argument('--remote-dir', type=str,
        help='remote folder in bucket')
    
    args = parser.parse_args()

    _yaml_to_env(args.yaml_file, args.env_file, args.data_path)
    _train()
    _upload_local_directory_to_minio("train_res/ds_tc_resnet/non_stream", 
    args.bucket_name, args.remote_dir)





