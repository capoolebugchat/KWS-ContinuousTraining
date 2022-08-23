from collections import namedtuple
import glob
import yaml
import logging
import kfp
import kfp.v2.dsl as dsl
from kfp.v2.dsl import (
    Input, Output, Artifact, Model, Dataset,component)
from typing import NamedTuple, Optional


@component(
    output_component_file="components/init_artifacts/component_SDKv2.yaml"
)
def init_artifacts(
    config_path: str,
    dataset_path: str,
    bucket_name: str,
    version: Optional[str],
    train_config: Output[Artifact],
    train_dataset: Output[Dataset],
):
    
    train_config.metadata = {"version":version, "local_path":config_path}
    # train_config.path = config_path
    train_dataset.metadata= {"version":version, "local_path":dataset_path}
    # train_dataset.path = dataset_path

    # from collections import namedtuple
    # _output = namedtuple(
    #   'InitArtifacts',['train_config', 'train_dataset'])
    
    # return _output(train_config=config, train_dataset=dataset)