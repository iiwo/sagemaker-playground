from __future__ import annotations

import json
import logging
import re
from typing import Union

from langchain.schema import AgentAction, AgentFinish, OutputParserException
from langchain.agents.structured_chat.output_parser \
    import StructuredChatOutputParser as LangchainStructuredChatOutputParser
from langchain.agents import AgentType, initialize_agent

logger = logging.getLogger(__name__)

B_BLOCK, E_BLOCK = "<s>", "</s>"
B_INST, E_INST = "[INST]", "[/INST]"
B_SYS, E_SYS = "<<SYS>>\n", "\n<</SYS>>\n\n"

PREFIX = B_BLOCK + B_INST + B_SYS + """
You are a JSON generator designed to assist with a wide range of tasks using provided tools.
"""

FORMAT_INSTRUCTIONS = """

You only respond using this format:
```json
{{{{ "action": TOOL_NAME, "action_input": TOOL_ARGUMENTS }}}}
```

Never use the same tool with same params more than one time.
""" + E_SYS + E_INST

SUFFIX = """"""

HUMAN_MESSAGE_TEMPLATE = (
    E_BLOCK + "{agent_scratchpad}" + B_BLOCK +
    "Use a tool to get more information OR send me the final answer " +
    "using final_answer if you have enough information to answer. " +
    "Remember to use JSON! \n\nQuestion: {input}\n\nAnswer: \n\n"
)


class StructuredChatOutputParser(LangchainStructuredChatOutputParser):
    """Output parser for the structured chat agent."""

    pattern = re.compile(r"(\{(?:(?!{).)*\"action\"[^{}]*(?:\{[^{}]*\}[^{}]*?)*\})", re.DOTALL)

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        try:
            action_matches = self.pattern.findall(text)
            if len(action_matches) > 0:
                if len(action_matches) > 1:
                    logger.warning("Got multiple actions: %s", action_matches)
                action_match = action_matches[-1]
                response = json.loads(action_match.group(1).strip(), strict=False)
                if isinstance(response, list):
                    logger.warning("Got multiple action responses: %s", response)
                    response = response[-1]
                if response["action"] == "final_answer":
                    return AgentFinish({"output": response["action_input"]}, text)
                else:
                    return AgentAction(
                        response["action"], response.get("action_input", {}), text
                    )
            else:
                return AgentFinish({"output": text}, text)
        except Exception as e:
            raise OutputParserException(f"Could not parse LLM output: {text}") from e


class LLamaAgent:
    def __new__(cls, llm, options=None, tools=None):
        if options is None:
            options = {}
        if tools is None:
            tools = []

        return initialize_agent(
            tools,
            llm,
            agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            max_iterations=3,
            verbose=True,
            handle_parsing_errors=True,
            early_stopping_method='generate',
            agent_kwargs={
                'output_parser': StructuredChatOutputParser(),
                'prefix': PREFIX,
                'suffix': SUFFIX,
                'format_instructions': FORMAT_INSTRUCTIONS,
                'human_message_template': HUMAN_MESSAGE_TEMPLATE,
                'ai_prefix': 'Assistant',
                'human_prefix': 'User'
            },
            ai_prefix='Assistant',
            human_prefix='User',
            **options
        )

