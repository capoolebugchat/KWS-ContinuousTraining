import kfp
import kfp.v2.dsl as dsl
from kfp.v2.dsl import (
    Input, Output, Artifact, Model, Dataset,component)
#TODO: version and upload model with respective 

def register_model_to_S3(
    model: Input[Model]
):
    
    import minio

    model.metadata["remote"]
