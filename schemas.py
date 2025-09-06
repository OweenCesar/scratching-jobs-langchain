from typing import List
from pydantic import BaseModel, Field

# field : let add extra information to the model, any constraint we want to add
# Base model: let us define our own


class Source(BaseModel):
    "Schema for a source in the response, it will be propagated to the agent"

    url: str = Field(description="The URL of the source")


class AgentResponse(BaseModel):
    "Schema for the response from the Tavily Search"

    answer: str = Field(description="The agent to the query")
    sources: List[Source] = Field(
        description="List of sources used to generate the answer",
        default_factory=list,  # with default factory we ensure that each instance gets its own fresh list
    )
