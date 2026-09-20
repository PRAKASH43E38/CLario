from typing import Annotated, TypedDict, List, Optional, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field

# --- State Definitions ---

class AgentOutput(BaseModel):
    agent_name: str
    content: str
    structured_data: Optional[Any] = None
    reasoning: Optional[str] = None

class CLARIOState(TypedDict):
    # The conversation history (messages)
    messages: Annotated[list, add_messages]
    
    # Current active session context
    session_id: int
    user_id: int
    
    # The dynamic roadmap
    roadmap_id: Optional[int]
    current_node_id: Optional[int]
    
    # Learner's current state (hypothesized or evidenced)
    learner_state: dict
    
    # The laest agent output
    last_output: Optional[AgentOutput]
    
    # Control flags
    next_step: str # e.g., "research", "teach", "evaluate", "complete"

# --- Agent Contracts (Pydantic) ---

class RoadmapNodeSchema(BaseModel):
    concept: str = Field(..., description="The core concept to be learned")
    objective: str = Field(..., description="What the learner should be able to do")
    activity_type: str = Field(..., description="Type: explanation, reasoning, application, assessment")
    difficulty: str = Field(..., description="easy, medium, hard")
    estimated_minutes: int = Field(..., description="Estimated time to complete")

class RoadmapSchema(BaseModel):
    title: str
    objective: str
    nodes: List[RoadmapNodeSchema]

class TeachingResponseSchema(BaseModel):
    explanation: str = Field(..., description="The adaptive explanation of the concept")
    analogy: Optional[str] = Field(None, description="A simple analogy to make it click")
    hint: Optional[str] = Field(None, description="A hint for the learner if they are stuck")
    interaction_prompt: str = Field(..., description="The question or task for the learner")
