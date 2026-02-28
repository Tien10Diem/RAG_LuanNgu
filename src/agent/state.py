from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
from operator import add as add_messages

class stateAgent(TypedDict):
    messages: Annotated[Sequence[BaseMessage],add_messages] 
    