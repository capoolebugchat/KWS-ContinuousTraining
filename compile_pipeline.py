import kfp
from kfp.components import load_component_from_file
import kfp.v2.dsl as dsl
from kfp.v2.dsl import Model, Dataset, Artifact
from kfp.compiler import Compiler
from kfp.onprem import mount_pvc

init_op = load_component_from_file("components/0_init_artifacts/component_SDKv2.yaml")
ingest_data_op = load_component_from_file("components/1_ingest_n_validate_data/component_SDKv2.yaml")
train_op = load_component_from_file("components/2_train/component_SDKv2.yaml")
deploy_op = load_component_from_file("components/4_deploy/component_SDKv2.yaml")

@dsl.pipeline(
    name="KWS-CT-Pipeline",
    description="KWS auto training pipeline. Accept minio data folder, manually upload model and artifacts to minio"
)
def pipeline(
    # config_file_url: str = "h_param.yaml",
    dataset_uri: str = "test_dataset",
    model_s3_bucket: str = "mlpipeline",
):
    # init_task = init_op(
    #     config_path = config_file_url,
    #     dataset_path = dataset_path,
    #     version = "v0.0.1")
    train_task = train_op(
        model_s3_bucket = model_s3_bucket,
        dataset_location = "/workspace/train_dataset/test-train-dataset"
    )
    train_task.apply(mount_pvc(
        pvc_name="example-dataset",
        volume_name="dataset",
        volume_mount_path="/workspace/train_dataset"
    ))
    # ingest_data_task = ingest_data_op(dataset_uri)
    # deploy_task = deploy_op(
    #     model = train_task.outputs["model"]
    # )

#mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE

kfp.compiler.Compiler(mode=kfp.dsl.PipelineExecutionMode.V2_COMPATIBLE).compile(
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