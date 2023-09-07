import boto3

client = boto3.client('sagemaker-runtime')
payload = 'Translate to German: How are you?'

response = client.invoke_endpoint(
    EndpointName='remote-endpoint',
    Body=payload,
    ContentType='application/json'
)

response_txt = response['Body'].read().decode('utf-8')

print(response_txt)
