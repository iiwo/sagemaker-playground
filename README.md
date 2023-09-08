An example of local/remote Sagemaker [t5-small](https://huggingface.co/t5-small) model deploy with integration examples

![img](img/Sagemaker%20integration.drawio.png)

## Prerequisites
- Python
- Poetry
- Docker
- AWS account configured

## Install dependencies

```shell
poetry install
```

## Role creation

see https://docs.aws.amazon.com/sagemaker/latest/dg/sagemaker-roles.html

## Authenticate your Docker client to ECR
see
- https://github.com/aws/deep-learning-containers/
- https://github.com/aws/deep-learning-containers/blob/master/available_images.md

```shell
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 763104351884.dkr.ecr.us-east-1.amazonaws.com
```

## Download and save the Model
```shell
poetry run python create_model.py
```

## Create a Tarball of the Model:
```shell
tar -czvf t5-small.tar.gz -C ./t5-small .
```

## Deploy model in local mode

```shell
poetry run python t5_local_deploy.py
```

## Deploy to Sagemaker Endpoint

```shell
poetry run python t5_remote_deploy.py
```

## Examples

### Python Example
```shell
poetry run python example_python.py
```

### Langchain Example
```shell
poetry run python example_langchain.py
```

### Local Request Example
```shell
poetry run python example_local_request.py
```

### Javascript Example
```shell
node example_javascript.js
```