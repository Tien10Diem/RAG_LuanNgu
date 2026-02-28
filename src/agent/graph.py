from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END 
from src.agent.nodes import call_llm, should_cont, action_node
from src.agent.state import stateAgent
import uuid

graph = StateGraph(stateAgent)

graph.add_node('call_llm', call_llm)
graph.add_node('action', action_node)
graph.add_conditional_edges(
    'call_llm',
    should_cont,
    {
        'action': 'action',
        END: END
    }
)

graph.add_edge(START, 'call_llm')
graph.add_edge('action', 'call_llm')

memory= MemorySaver()
rag= graph.compile(checkpointer=memory)

random_uuid = uuid.uuid4()
config = {"configurable": {"thread_id": str(random_uuid)}}

