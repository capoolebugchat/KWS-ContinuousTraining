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
    version: Optional[str],
    train_config: Output[Artifact],
    train_dataset: Output[Dataset],
) -> None:
    
    train_config.metadata = {"version":version, "local_path":config_path}
    train_dataset.metadata= {"version":version, "local_path":dataset_path}
       
    import os
    os.system("printenv")