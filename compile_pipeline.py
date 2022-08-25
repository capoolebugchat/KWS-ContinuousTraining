import kfp
from kfp.components import load_component_from_file
import kfp.dsl as dsl
from kfp.v2.dsl import Model, Dataset, Artifact

init_op = load_component_from_file("components/init_artifacts/component_SDKv2.yaml")
train_op = load_component_from_file("components/train/component_SDKv2.yaml")
deploy_op = load_component_from_file("components/deploy/component_SDKv2.yaml")

@dsl.pipeline(
    name="KWS-train-test-pipe"
)
def pipeline(
    config_file_url: str = "h_param.yaml",
    dataset_path: str = "test_dataset",
    model_S3_bucket: str = "model-store",
):
    init_task = init_op(
        config_path = config_file_url,
        dataset_path = dataset_path,
        version = "v0.0.1")
    train_task = train_op(
        model_S3_bucket = model_S3_bucket,
        dataset = init_task.outputs["train_dataset"],
        config = init_task.outputs["train_config"]
    )
    deploy_task = deploy_op(
        model = train_task.outputs["model"]
    )

kfp.compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(
    pipeline_func=pipeline,
    package_path='pipeline.yaml')