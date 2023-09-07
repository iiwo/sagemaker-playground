from typing import Dict

from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler


class ContentHandler(LLMContentHandler):
    content_type = 'application/json'
    accepts = 'application/json'

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        return prompt.encode('utf-8')

    def transform_output(self, output: bytes) -> str:
        return output.read().decode('utf-8')


content_handler = ContentHandler()
llm = SagemakerEndpoint(
    endpoint_name='remote-endpoint',
    region_name='us-east-2',
    content_handler=content_handler
)

result = llm.invoke('Translate to German: How are you?')
print(result)
