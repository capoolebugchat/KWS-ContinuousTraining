import kfp
import kfp.v2.dsl as dsl
from kfp.v2.dsl import (
    Input, Output, Artifact, Model, Dataset,component)
from typing import NamedTuple, Optional

@component(
    packages_to_install = [
        "kserve==0.8.0",
        "kubernetes==18.20.0",
        ],
    output_component_file = "components/deploy/component_SDKv2.yaml"
)
def deploy(
    model: Input[Model],
):

    import logging
    from kubernetes import client
    import kserve
    from kserve import KServeClient
    from kserve import constants
    from kserve import V1beta1PredictorSpec
    from kserve import V1beta1TFServingSpec
    from kserve import V1beta1InferenceServiceSpec
    from kserve import V1beta1InferenceService

    default_model_spec = V1beta1InferenceServiceSpec(
        predictor=V1beta1PredictorSpec(
            tensorflow=V1beta1TFServingSpec(
                storage_uri=model.metadata["S3_URI"]
                )
            )
        )

    isvc = V1beta1InferenceService(
        api_version=constants.KSERVE_V1BETA1,
        kind=constants.KSERVE_KIND,
        metadata=client.V1ObjectMeta(
            name='auto-deployed-model', 
            namespace='kubeflow-user-example-com'
            ),
            spec=default_model_spec
        )

    client = KServeClient()
    client.set_credentials(
        storage_type = "S3",
        namespace = "kubeflow-user-example-com",
        service_account = "default-editor"
    )
    '''mlpipeline-minio-artifact -n kubeflow-user-example-com'''
    logging.info("Client created")

    client.create(isvc)
    logging.info("ISVC created. Object sent to K8s apiserver")
    
    client.wait_isvc_ready(
        name = 'auto-deployed-model',
        namespace = 'kubeflow-user-example-com',
        timeout_seconds = 300
        )
    logging.info("ISVC ready. Model deployed")