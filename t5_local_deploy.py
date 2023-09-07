from sagemaker.local import LocalSession
from sagemaker.pytorch import PyTorchModel

sagemaker_local_session = LocalSession()
sagemaker_local_session.config = {'local': {'local_code': True}}

role = 'arn:aws:iam::123456789012:role/SageMaker-Execution'  # Replace with your SageMaker IAM role

pytorch_model = PyTorchModel(
    model_data='file://t5-small.tar.gz',
    role=role,
    framework_version='2.0.0',
    py_version='py3',
    entry_point='t5-small.py',
    image_uri='763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:2.0.0-transformers4.28.1-cpu-py310-ubuntu20.04',
    sagemaker_session=sagemaker_local_session
)

predictor = pytorch_model.deploy(
    instance_type='local',
    initial_instance_count=1,
    endpoint_name='local-endpoint'
)
