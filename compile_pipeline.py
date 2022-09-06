import kfp
from kfp.components import load_component_from_file
import kfp.dsl as dsl
from kfp.dsl import Model, Dataset, Artifact
from kfp.compiler import Compiler

init_op = load_component_from_file("components/init_artifacts/component_SDKv2b4.yaml")
train_op = load_component_from_file("components/train/component_SDKv2b4.yaml")
deploy_op = load_component_from_file("components/deploy/component_SDKv2b4.yaml")
print(train_op.__str__)
@dsl.pipeline(
    name="KWS-train-test-pipe",
    
)
def pipeline(
    config_file_url: str = "h_param.yaml",
    dataset_path: str = "test_dataset",
    model_s3_bucket: str = "mlpipeline",
):
    init_task = init_op(
        config_path = config_file_url,
        dataset_path = dataset_path,
        version = "v0.0.1")
    train_task = train_op(
        model_S3_bucket = model_s3_bucket,
        config = init_task.outputs["train_config"],
        dataset = init_task.outputs["train_dataset"]
    )
    # deploy_task = deploy_op(
    #     model = train_task.outputs["model"]
    # )

#mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE

kfp.compiler.Compiler().compile(
    pipeline_func=pipeline,
    package_path='pipeline.yaml')