'''
# python3.13 -m venv .venv && source .venv/bin/activate
# pip install -r requirements.txt
'''
# LangGraph Multi-Agent Travel Booking System with In-Memory SQLite Memory

# main.py

import os
import sqlite3
from typing import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
)

from langchain_groq import ChatGroq

from tools.tavily_tool import tavily_search
from tools.flight_tool import search_flights
from dotenv import load_dotenv
load_dotenv()

# LLM — llama-3.3-70b-versatile is enterprise-only on Groq now
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
)

# State
class TravelState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_query: str
    origin_city: str
    flight_results: str
    hotel_results: str
    itinerary: str
    llm_calls: int

# Flight Agent
def flight_agent(state: TravelState):
    query = state["user_query"]
    origin = (state.get("origin_city") or "").strip()
    flight_data = search_flights(query, origin=origin)
    return {
        "flight_results": flight_data,
        "messages": [
            AIMessage(content=f"Flight results fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Hotel Agent
def hotel_agent(state: TravelState):
    query = f"Best hotels for {state['user_query']}"
    hotel_results = tavily_search(query)

    return {
        "hotel_results": hotel_results,
        "messages": [
            AIMessage(content="Hotel information fetched")
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Itinerary Agent
def itinerary_agent(state: TravelState):

    prompt = f"""
    Create a travel itinerary.
    Starting city (traveller origin): {state.get("origin_city") or "not provided"}
    User Query:
    {state["user_query"]}

    Flight Results:
    {state["flight_results"]}

    Hotel Results:
    {state["hotel_results"]}

    Plan outbound travel FROM the starting city to the destination.
    Do not assume a different origin.
    """

    response = llm.invoke([
        SystemMessage(
            content="You are an expert travel planner"
        ),
        HumanMessage(content=prompt)
    ])

    return {
        "itinerary": response.content,
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# Final Response Agent
def final_agent(state: TravelState):

    final_prompt = f"""
    Generate final travel response.
    Starting city (traveller origin): {state.get("origin_city") or "not provided"}

    Flights:
    {state["flight_results"]}

    Hotels:
    {state["hotel_results"]}

    Itinerary:
    {state["itinerary"]}

    Keep flights and the itinerary consistent with departing from the starting city.
    """

    response = llm.invoke([
        HumanMessage(content=final_prompt)
    ])

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


graph = StateGraph(TravelState)

graph.add_node("flight_agent", flight_agent)
graph.add_node("hotel_agent", hotel_agent)
graph.add_node("itinerary_agent", itinerary_agent)
graph.add_node("final_agent", final_agent)

graph.add_edge(START, "flight_agent")
graph.add_edge("flight_agent", "hotel_agent")
graph.add_edge("hotel_agent", "itinerary_agent")
graph.add_edge("itinerary_agent", "final_agent")
graph.add_edge("final_agent", END)


# In-memory SQLite so both CLI and Streamlit can share the compiled app
# check_same_thread=False is required because LangGraph may use the connection
# from worker threads; SqliteSaver serializes access with an internal lock.
_conn = sqlite3.connect(":memory:", check_same_thread=False)
checkpointer = SqliteSaver(_conn)
checkpointer.setup()

app = graph.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        running_in_streamlit = get_script_run_ctx() is not None
    except Exception:
        running_in_streamlit = False

    if running_in_streamlit:
        import streamlit as st

        st.set_page_config(page_title="Travel Planner", layout="wide")
        st.error(
            "This deployment is running `main.py`, which is the terminal CLI. "
            "In Streamlit Cloud go to **⋮ → Settings → Main file path** and set it to "
            "`frontend.py` or `streamlit_app.py`, then reboot."
        )
        st.stop()

    config = {
        "configurable": {
            "thread_id": "user_aarohi"
        }
    }

    user_input = input("Enter travel request: ")

    result = app.invoke(
        {
            "messages": [
                HumanMessage(content=user_input)
            ],
            "user_query": user_input,
            "origin_city": "",
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "llm_calls": 0
        },
        config=config
    )

    print("\nFINAL RESPONSE:\n")

    for msg in result["messages"]:
        print(msg.content)
