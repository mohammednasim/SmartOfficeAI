from langgraph.graph import StateGraph, START, END

from graph.state import AgentState
from graph.nodes import (
    router_node,
    calculator_node,
    sql_node,
    email_node,
    calendar_node,
    chatbot_node
)

# Create the graph
builder = StateGraph(AgentState)

# Add all nodes
builder.add_node("router", router_node)
builder.add_node("calculator", calculator_node)
builder.add_node("sql", sql_node)
builder.add_node("email", email_node)
builder.add_node("calendar", calendar_node)
builder.add_node("chatbot", chatbot_node)

# Set entry point
builder.add_edge(START, "router")

# Add conditional routing from router
builder.add_conditional_edges(
    "router",
    lambda state: state["next"],
    {
        "calculator": "calculator",
        "sql": "sql",
        "email": "email",
        "calendar": "calendar",
        "chatbot": "chatbot"
    }
)

# All tool nodes end the conversation
builder.add_edge("calculator", END)
builder.add_edge("sql", END)
builder.add_edge("email", END)
builder.add_edge("calendar", END)
builder.add_edge("chatbot", END)

# Compile the graph
graph = builder.compile()