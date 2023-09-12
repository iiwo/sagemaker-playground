import boto3
import json

client = boto3.client('sagemaker-runtime')
payload = {
    'inputs': "Simply put, the theory of relativity states that",
    'parameters': {
        'max_new_tokens': 512,
        'top_p': 0.9,
        'temperature': 0.6,
        'return_full_text': False
    }
}

response = client.invoke_endpoint(
    EndpointName='ENDPOINT_NAME',
    Body=json.dumps(payload),
    ContentType='application/json',
    CustomAttributes='accept_eula=true'
)

response_txt = response['Body'].read().decode('utf-8')

print(response_txt)
