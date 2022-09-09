from collections import namedtuple
import kfp
import kfp.v2.dsl as dsl
from kfp.v2.dsl import (
    Input, Output, Artifact, Model, Dataset,component)
import time
import logging
import os
from typing import Optional

print(os.system("pwd"))
@component(
    output_component_file="components/0_init_artifacts/component_SDKv2.yaml"
)
def init_artifacts(
    config_path: str,
    dataset_path: str,
    version: Optional[str],
    train_dataset: Output[Dataset],
    train_config: Output[Artifact]
):
    
    import logging
    import os

    os.listdir()

    os.listdir("/")
    logging.info("dataset.path:"+train_dataset.path)
    logging.info(train_dataset.metadata)
    logging.info("config.path:"+train_config.path)
    logging.info(train_config.metadata)

    train_config.metadata = {"version":version, "local_path":config_path}
    train_dataset.metadata= {"version":version, "local_path":dataset_path}
       
    import os
    os.system("printenv")

# V2 COMPILATION
# from kfp.compiler import Compiler
# Compiler().compile(
#     pipeline_func=init_artifacts,
#     package_path="components/0_init_artifacts/component_SDKv2b4.yaml"
# )