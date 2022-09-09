from importlib.resources import path
from re import L
from typing import Any
import kfp
import kfp.v2.dsl as dsl
from kfp.v2.dsl import (
    Input, Output, Artifact, Model, Dataset,component)

@component
def ingest_data_to_local_dir(
    dataset_uri: str,
    dataset_path: str,
    dataset: Output[Dataset],
    # data_report: Output[Artifact] 
):
#-> Output[Dataset]: Actual Dataset, downloaded to root dir and validated
#-> Output[Artifact]: Data report: count, 
# splits, tr-words count(all & in split), tr-words.

    import logging
    import os

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
    
    def _parse_uri(uri:str):        
        dataset_info = {}
        
        if uri.split(":")[0]=="minio":
            uri_segments = uri[:8].split('/')
            dataset_info["bucket_name"] = uri_segments[0]
            dataset_info["directory"] = os.path.join(*uri_segments[1:])
        else: 
            logging.info("wrong URI format, should be minio://bucket/folder/...")
        return dataset_info

    def _validate_datapoint(
        datapoint_path:Any,
        dataset_info: dict
    ):
    #TODO: this is not optimal, consider numpy-like parrallelism
        datapoint_path = str(datapoint_path)
        if "/training/" in datapoint_path: 
            dataset_info["train_split"]["count"]["total"]+=1
            if "/trigger/" in datapoint_path: dataset_info["train_split"]["count"]["trigger"]+=1
            elif "/non-trigger/" in datapoint_path: dataset_info["train_split"]["count"]["non-trigger"]+=1
        elif "/testing/" in datapoint_path: 
            dataset_info["test_split"]["count"]["total"]+=1
            if "/trigger/" in datapoint_path: dataset_info["test_split"]["count"]["trigger"]+=1
            elif "/non-trigger/" in datapoint_path: dataset_info["test_split"]["count"]["non-trigger"]+=1
        elif "/validation/" in datapoint_path: 
            dataset_info["val_split"]["count"]["total"]+=1
            if "/trigger/" in datapoint_path: dataset_info["val_split"]["count"]["trigger"]+=1
            elif "/non-trigger/" in datapoint_path: dataset_info["val_split"]["count"]["non-trigger"]+=1
        elif "_background_noise_" in datapoint_path:
            dataset_info["count"]+=1
        else : 
            logging.info(f"Not a valid datapoint, path: {datapoint_path}")
            return False
        return True

    def download_entire_dataset(
        _uri:str,
        local_storage_dir:str
        ):
    #-> download dataset to pipeline root, all while count dataset, source: minio

        dataset_info = _parse_uri(_uri)
        dataset_info["train_split"] = {}
        dataset_info["test_split"] = {}
        dataset_info["val_split"] = {}
        dataset_info["count"] = 0
        dataset_info["train_split"]["count"] = {"total":0, 
                                                "trigger":0, "non-trigger":0}
        dataset_info["test_split"]["count"] = {"total":0, 
                                                "trigger":0, "non-trigger":0}
        dataset_info["val_split"]["count"] = {"total":0, 
                                                "trigger":0, "non-trigger":0}
        
        for item in minio_client.list_objects(
            bucket_name = dataset_info["bucket_name"],
            prefix      = dataset_info["directory"],
            recursive   = True
            ):

            if _validate_datapoint(
                datapoint_path = item.object_name,
                dataset_info = dataset_info
                ):
                
                minio_client.fget_object(
                    bucket_name = dataset_info["bucket_name"],
                    object_name = item.object_name,
                    file_path   = os.path.join(dataset.path,item.object_name)
                )

            else:
                continue
        
        return dataset_info
    
    logging.info("Start downloading and validating dataset, each sample")
    dataset_info = download_entire_dataset(
        _uri = dataset_uri,
        local_storage_dir = dataset_path,
    )
    
    dataset.name = "AudioDataset"
    dataset.metadata = dataset_info
    dataset.metadata["origin"] = dataset_uri
    dataset.metadata["local_path"] = dataset_path


from kfp.compiler import Compiler
Compiler().compile(
    pipeline_func=ingest_data_to_local_dir,
    package_path="components/1_ingest_n_validate_data/component_SDKv2b4.yaml"
)
