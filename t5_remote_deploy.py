import sagemaker
from sagemaker.pytorch import PyTorchModel

sagemaker_session = sagemaker.Session()

role = 'arn:aws:iam::123456789012:role/SageMaker-Execution'  # Replace with your SageMaker IAM role

pytorch_model = PyTorchModel(
    model_data='file://t5-small.tar.gz',
    role=role,
    framework_version='2.0.0',
    py_version='py3',
    entry_point='t5-small.py',
    image_uri='763104351884.dkr.ecr.us-east-1.amazonaws.com/huggingface-pytorch-inference:2.0.0-transformers4.28.1-cpu-py310-ubuntu20.04',
    sagemaker_session=sagemaker_session
)


predictor = pytorch_model.deploy(
    initial_instance_count=1,
    instance_type='ml.m5.xlarge',
    endpoint_name='remote-endpoint'
)
