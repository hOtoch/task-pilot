from typing import TypedDict, List, Dict, Any, Annotated
import operator


class AgentState(TypedDict):
    project_idea: str
    tasks: Annotated[List[dict], operator.add] # (Annotated para permitir append progressivo se necessário)
    platform: str
    status: str
    