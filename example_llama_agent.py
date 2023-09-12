import json
from typing import Dict

import logging
import langchain

from langchain import SagemakerEndpoint
from langchain.llms.sagemaker_endpoint import LLMContentHandler
from langchain.tools import DuckDuckGoSearchResults

from llama_agent import LLamaAgent

log_level = logging.DEBUG
logging.basicConfig(level=log_level)
langchain.debug = log_level == logging.DEBUG


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
    model_kwargs={
        'max_new_tokens': 512,
        'top_p': 0.9,
        'temperature': 0.001
    },
    endpoint_kwargs={'CustomAttributes': 'accept_eula=true'}
)

agent = LLamaAgent(llm, tools=[DuckDuckGoSearchResults(backend="news")])
agent.run('What is the top news in tech today?')
