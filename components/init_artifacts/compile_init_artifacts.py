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
    output_component_file="component_SDKv2.yaml"
)
def init_artifacts(
    config_file_url: str,
    dataset_path: str,
    bucket_name: str,
    version: Optional[str]
)->NamedTuple(
  'ExampleOutputs',[
    ('config', Artifact),
    ('dataset', Dataset)]
):
    
    config = Artifact(name="train_config", uri=config_file_url)
    dataset = Dataset(name="train_dataset", uri=dataset_path)

    from collections import namedtuple
    _output = namedtuple(
      'InitArtifacts',['config', 'dataset'])
    
    return _output(config=config, dataset=dataset)