import json
from typing import Dict

from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler


class ContentHandler(LLMContentHandler):
    content_type = 'application/json'
    accepts = 'application/json'

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        payload = {
            'inputs': prompt,
            'parameters': {
                **model_kwargs
            }
        }

        return json.dumps(payload).encode('utf-8')

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode('utf-8'))
        return response_json [0]['generation']


content_handler = ContentHandler()
llm = SagemakerEndpoint(
    endpoint_name='ENDPOINT_NAME',
    region_name='us-east-1',
    content_handler=content_handler,
    endpoint_kwargs={'CustomAttributes': 'accept_eula=true'}
)

result = llm.invoke("Simply put, the theory of relativity states that")
print(result)
