from typing import Annotated
from typing_extensions import TypedDict,Literal,Union
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]
    # query_type: Literal["chat", "web"]
    # url: Union[str, None]