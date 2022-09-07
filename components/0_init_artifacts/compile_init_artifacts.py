from collections import namedtuple
import glob
import yaml
import logging
import kfp
import kfp.dsl as dsl
from kfp.dsl import (
    Input, Output, Artifact, Model, Dataset,component)
from typing import NamedTuple, Optional


@component(
    # output_component_file="components/init_artifacts/component_SDKv2.yaml"
)
def init_artifacts(
    config_path: str,
    dataset_path: str,
    version: Optional[str],
    train_config: Output[Artifact],
    train_dataset: Output[Dataset],
) -> None:
    
    import logging

    logging.info("dataset.path:"+train_dataset.path)
    logging.info(train_dataset.metadata)
    logging.info("config.path:"+train_config.path)
    logging.info(train_config.metadata)

    train_config.metadata = {"version":version, "local_path":config_path}
    train_dataset.metadata= {"version":version, "local_path":dataset_path}
       
    import os
    os.system("printenv")

from kfp.compiler import Compiler
Compiler().compile(
    pipeline_func=init_artifacts,
    package_path="components/0_init_artifacts/component_SDKv2b4.yaml"
)