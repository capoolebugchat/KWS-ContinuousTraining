import os
from minio import Minio
import argparse
import glob
import logging

client = Minio(
        "minio-service.kubeflow.svc.cluster.local:9000",
        access_key="minio",
        secret_key="minio123",
        secure=False
    )

def upload_local_directory_to_minio(local_path, bucket_name, minio_path):
    assert os.path.isdir(local_path)

    for local_file in glob.glob(local_path + '/**'):
        local_file = local_file.replace(os.sep, "/") # Replace \ with / on Windows
        if not os.path.isfile(local_file):
            upload_local_directory_to_minio(
                local_file, bucket_name, minio_path + "/" + os.path.basename(local_file))
        else:
            remote_path = os.path.join(
                minio_path, local_file[1 + len(local_path):])
            remote_path = remote_path.replace(
                os.sep, "/")  # Replace \ with / on Windows
            client.fput_object(bucket_name, remote_path, local_file)

parser = argparse.ArgumentParser(description='None')

parser.add_argument('--local-dir', type=str,
    help='local folder to upload')
parser.add_argument('--bucket-name', type=str,
    help='Name of the Minio bucket')
parser.add_argument('--remote-dir', type=str,
    help='remote folder in bucket')
args = parser.parse_args()

logging.info(f"Folder {args.local_dir} is being added as {args.remote_dir}")
upload_local_directory_to_minio(args.local_dir, args.bucket_name, args.remote_dir)
logging.info("Adding succeeded")