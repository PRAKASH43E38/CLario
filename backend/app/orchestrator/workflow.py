from typing import Annotated, TypedDict
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from app.ai.agents import NovaResearchAgent
from app.ai.cala import LearnerContext, create_learner_context
from app.ai.prompts import roadmap_prompt
from app.ai.router import build_provider_router
from app.models.learner import LearningSession
from app.schemas.learning import RoadmapPlan


class LearningWorkflowState(TypedDict, total=False):
    messages: Annotated[list, add_messages]
    task: str
    goal: str
    learner_state: str
    interests: str
    learner_context: LearnerContext
    requires_research: bool
    research_context: str
    roadmap_plan: RoadmapPlan
    current_step: str


def _needs_research(task: str, goal: str) -> bool:
    freshness_terms = ("latest", "current", "recent", "today", "news", "updated", "research", "benchmark", "state of the art")
    text = f"{task} {goal}".lower()
    return any(term in text for term in freshness_terms)


async def route_node(state: LearningWorkflowState) -> LearningWorkflowState:
    learner_context = create_learner_context(state["task"], state["goal"], state["learner_state"], state.get("interests"))
    return {
        "learner_context": learner_context,
        "requires_research": _needs_research(state["task"], state["goal"]),
        "current_step": "routing",
    }


async def research_node(state: LearningWorkflowState) -> LearningWorkflowState:
    try:
        agent = NovaResearchAgent()
        learner_context = state.get("learner_context") or create_learner_context(state["task"], state["goal"], state["learner_state"], state.get("interests"))
        query = f"{learner_context.topic} {learner_context.goal} beginner explanation for {learner_context.interest}"
        context = await agent.execute_research(query, learner_context=learner_context, stage="roadmap")
        return {"research_context": context, "current_step": "researched"}
    except Exception as e:
        return {"research_context": f"Research failed: {str(e)}", "current_step": "research_failed"}


async def plan_node(state: LearningWorkflowState) -> LearningWorkflowState:
    session = LearningSession(
        task=state["task"],
        goal=state["goal"],
        learner_state=state["learner_state"],
        interests=state["interests"],
    )
    learner_context = state.get("learner_context") or create_learner_context(state["task"], state["goal"], state["learner_state"], state.get("interests"))
    prompt = roadmap_prompt(session)
    prompt += "\n\n" + learner_context.to_prompt_context() + "\n"
    if state.get("research_context"):
        prompt += f"\n\n{state['research_context']}"

    router = build_provider_router()
    plan = await router.generate_structured(prompt, RoadmapPlan)
    return {"roadmap_plan": plan, "current_step": "planned"}


def _research_branch(state: LearningWorkflowState) -> str:
    return "research" if state.get("requires_research") else "plan"


def build_learning_graph():
    graph = StateGraph(LearningWorkflowState)
    graph.add_node("route", route_node)
    graph.add_node("research", research_node)
    graph.add_node("plan", plan_node)

    graph.set_entry_point("route")
    graph.add_conditional_edges("route", _research_branch, {"research": "research", "plan": "plan"})
    graph.add_edge("research", "plan")
    graph.add_edge("plan", END)

    return graph.compile()


async def run_roadmap_workflow(session: LearningSession) -> LearningWorkflowState:
    graph = build_learning_graph()
    return await graph.ainvoke({
        "task": session.task,
        "goal": session.goal,
        "learner_state": session.learner_state,
        "interests": session.interests,
    })
