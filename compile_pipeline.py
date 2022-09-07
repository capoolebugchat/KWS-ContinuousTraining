import kfp
from kfp.components import load_component_from_file
import kfp.dsl as dsl
from kfp.dsl import Model, Dataset, Artifact
from kfp.compiler import Compiler

init_op = load_component_from_file("components/init_artifacts/component_SDKv2b4.yaml")
ingest_data_op = load_component_from_file("components/ingest_n_validate_data/component_SDKv2b4.yaml")
train_op = load_component_from_file("components/train/component_SDKv2b4.yaml")
deploy_op = load_component_from_file("components/deploy/component_SDKv2b4.yaml")

@dsl.pipeline(
    name="KWS-CT-Pipeline",
    description="KWS auto training pipeline. Accept minio data folder, manually upload model and artifacts to minio"
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

# local integration testing
# from kfp.deprecated import run_pipeline_func_locally

# result = run_pipeline_func_locally(
#     pipeline_func = pipeline,
#     arguments = {
#         "config_file_url":"h_param.yaml",
#         "dataset_path":"test_dataset",
#         "model_s3_bucket":"mlpipeline"
#     }
# )