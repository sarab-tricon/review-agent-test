from langgraph.graph import StateGraph
from typing import TypedDict, List, Dict, Any
from agents.code_analyzer import analyze_code
from agents.optimizer import optimize_code
from agents.security_checker import check_security
from agents.doc_checker import check_documentation
from utils.helpers import combine_reviews

class ReviewState(TypedDict):
    code_content: str
    analyzer_result: Dict[str, Any]
    optimizer_result: Dict[str, Any]
    security_result: Dict[str, Any]
    documentation_result: Dict[str, Any]
    final_review: Dict[str, Any]

def create_review_workflow():
    workflow = StateGraph(ReviewState)
    
    def analyzer_node(state):
        result = analyze_code(state["code_content"])
        state["analyzer_result"] = result
        return state
    
    def optimizer_node(state):
        result = optimize_code(state["code_content"])
        state["optimizer_result"] = result
        return state
    
    def security_node(state):
        result = check_security(state["code_content"])
        state["security_result"] = result
        return state
    
    def documentation_node(state):
        result = check_documentation(state["code_content"])
        state["documentation_result"] = result
        return state
    
    def combine_node(state):
        reviews = [
            state["analyzer_result"],
            state["optimizer_result"],
            state["security_result"],
            state["documentation_result"]
        ]
        combined = combine_reviews(reviews)
        state["final_review"] = combined
        return state
    
    workflow.add_node("analyzer", analyzer_node)
    workflow.add_node("optimizer", optimizer_node)
    workflow.add_node("security", security_node)
    workflow.add_node("documentation", documentation_node)
    workflow.add_node("combine", combine_node)
    
    workflow.set_entry_point("analyzer")
    
    workflow.add_edge("analyzer", "optimizer")
    workflow.add_edge("optimizer", "security")
    workflow.add_edge("security", "documentation")
    workflow.add_edge("documentation", "combine")
    
    workflow.set_finish_point("combine")
    
    return workflow.compile()