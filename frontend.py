import os
from datetime import datetime

import streamlit as st
from langchain_core.messages import HumanMessage

from main import app

st.set_page_config(
    page_title="Travel Planner",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Serif:wght@500;600&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"] {
    font-family: 'IBM Plex Sans', sans-serif;
    background: #f3f3f0;
    color: #1c1c1c;
    color-scheme: light;
}

.block-container {
    padding: 1.25rem 2rem 3rem !important;
    max-width: 1180px;
}

#MainMenu, footer, header,
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"],
[data-testid="stDecoration"] { display: none !important; visibility: hidden; }

.topbar {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 1rem;
    padding-bottom: 0.15rem;
}
.rule {
    border: 0;
    border-top: 1px solid #dcdcd6;
    margin: 0 0 1.4rem;
}
.brand {
    font-family: 'IBM Plex Serif', serif;
    font-size: 1.55rem;
    font-weight: 600;
    letter-spacing: -0.02em;
    color: #1c1c1c;
}
.brand-sub {
    margin: 0.15rem 0 0.4rem;
    font-size: 0.86rem;
    color: #6a6a66;
}
.kicker {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #6a6a66;
    margin: 0.4rem 0 0.5rem;
}
.examples {
    margin: 0 0 0.95rem;
}
.examples-title {
    font-size: 0.92rem;
    font-weight: 600;
    color: #1c1c1c;
    margin: 0 0 0.35rem;
}
.example {
    font-size: 0.84rem;
    color: #5c5c58;
    line-height: 1.45;
    padding: 0.22rem 0;
}
.agent-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0 0 1.1rem;
}
.agent-chip {
    display: inline-block;
    background: #fff;
    color: #1c1c1c;
    border: 1px solid #cfcfc8;
    border-radius: 4px;
    padding: 0.42rem 0.75rem;
    font-size: 0.82rem;
    font-weight: 500;
    pointer-events: none;
    cursor: default;
    user-select: none;
}
.powered {
    margin-top: 1.75rem;
    padding-top: 1rem;
    border-top: 1px solid #dcdcd6;
}
.powered-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
}
.city-row {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 0.55rem;
    margin: 0 0 1.35rem;
}
.city-card {
    position: relative;
    height: 92px;
    overflow: hidden;
    border: 1px solid #e2e2dc;
    background: #ddd;
}
.city-card img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
    filter: brightness(0.62);
}
.city-card span {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 8px;
    text-align: center;
    color: #fff;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.02em;
}
.metric-row { display: flex; gap: 0.75rem; margin: 1rem 0 1.25rem; }
.metric-box {
    flex: 1;
    border: 1px solid #e2e2dc;
    padding: 0.8rem 0.9rem;
    background: #fafaf7;
}
.metric-val { font-size: 1.35rem; font-weight: 600; color: #1c1c1c; }
.metric-lbl {
    font-size: 0.72rem;
    color: #6a6a66;
    margin-top: 0.15rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.save-bar {
    border: 1px solid #e2e2dc;
    background: #fafaf7;
    padding: 0.75rem 1rem;
    color: #4f4f4b;
    font-size: 0.86rem;
}
.save-bar code {
    background: #eee;
    color: #1c1c1c;
    padding: 0.1em 0.35em;
}

div[data-testid="stButton"] button,
div[data-testid="stFormSubmitButton"] button {
    background: #fff !important;
    color: #1c1c1c !important;
    border: 1px solid #cfcfc8 !important;
    border-radius: 4px !important;
    font-weight: 500 !important;
    box-shadow: none !important;
    padding: 0.45rem 0.7rem !important;
}
div[data-testid="stButton"] button:hover,
div[data-testid="stFormSubmitButton"] button:hover {
    background: #f0f0eb !important;
    border-color: #1c1c1c !important;
}
div[data-testid="stFormSubmitButton"] button[kind="primary"],
button[data-testid="stBaseButton-primary"],
div[data-testid="stFormSubmitButton"] button[kind="primaryFormSubmit"] {
    background: #1c1c1c !important;
    color: #fff !important;
    border-color: #1c1c1c !important;
}
div[data-testid="stDownloadButton"] button {
    background: #fff !important;
    color: #1c1c1c !important;
    border: 1px solid #cfcfc8 !important;
    border-radius: 4px !important;
}

[data-testid="stTextArea"] textarea,
.stTextArea textarea,
[data-baseweb="textarea"] textarea {
    background: #fff !important;
    border: 1px solid #cfcfc8 !important;
    border-radius: 4px !important;
    color: #1c1c1c !important;
    -webkit-text-fill-color: #1c1c1c !important;
    font-size: 0.95rem !important;
    caret-color: #1c1c1c !important;
}
[data-testid="stTextArea"] textarea:placeholder-shown,
.stTextArea textarea:placeholder-shown,
[data-baseweb="textarea"] textarea:placeholder-shown {
    color: #9a9a94 !important;
    -webkit-text-fill-color: #9a9a94 !important;
    font-style: italic !important;
}
[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stTextArea"] textarea::-webkit-input-placeholder,
.stTextArea textarea::placeholder,
textarea::placeholder {
    color: #9a9a94 !important;
    -webkit-text-fill-color: #9a9a94 !important;
    font-style: italic !important;
    opacity: 1 !important;
}
.stTextArea textarea:focus,
.stTextInput input:focus {
    border-color: #1c1c1c !important;
    box-shadow: none !important;
}
.stTextInput input {
    background: #fff !important;
    border: 1px solid #cfcfc8 !important;
    border-radius: 4px !important;
    color: #1c1c1c !important;
}
.stTextInput label, .stTextArea label {
    color: #4f4f4b !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

[data-testid="stStatusWidget"] {
    background: #fff !important;
    border: 1px solid #e2e2dc !important;
    border-radius: 4px !important;
}
.stAlert { background: #fafaf7 !important; border: 1px solid #e2e2dc !important; }
.stMarkdown p, .stMarkdown li, .stMarkdown td, .stMarkdown th { color: #2a2a28 !important; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #1c1c1c !important; }
</style>
""",
    unsafe_allow_html=True,
)

CITIES = [
    ("Tokyo", "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400&q=70"),
    ("Paris", "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400&q=70"),
    ("Bangkok", "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=400&q=70"),
    ("Rome", "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400&q=70"),
    ("Dubai", "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400&q=70"),
]

AGENT_META = {
    "flight_agent": ("1", "Flights"),
    "hotel_agent": ("2", "Hotels"),
    "itinerary_agent": ("3", "Itinerary"),
    "final_agent": ("4", "Final plan"),
}

if "trip_query" not in st.session_state:
    st.session_state.trip_query = ""
if "thread_id" not in st.session_state:
    st.session_state.thread_id = "kingsley_user"
if "plan" not in st.session_state:
    st.session_state.plan = None
if "form_error" not in st.session_state:
    st.session_state.form_error = ""

head_l, head_r = st.columns([3.2, 1.2], vertical_alignment="top")
with head_l:
    st.markdown(
        """
        <div class="topbar">
            <div>
                <div class="brand">Travel Planner</div>
                <div class="brand-sub">Four agents assemble flights, hotels, and a day-by-day itinerary.</div>
                <div class="agent-row">
                    <span class="agent-chip">Flight search Agent</span>
                    <span class="agent-chip">Hotel search Agent</span>
                    <span class="agent-chip">Itinerary draft Agent</span>
                    <span class="agent-chip">Combined response Agent</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with head_r:
    st.text_input(
        "Session ID",
        key="thread_id",
        help="Used as the LangGraph thread id so this session can keep memory.",
    )

city_html = '<div class="city-row">'
for name, url in CITIES:
    city_html += (
        f'<div class="city-card"><img src="{url}" alt="{name}" />'
        f"<span>{name}</span></div>"
    )
city_html += "</div>"
st.markdown(city_html, unsafe_allow_html=True)

left, right = st.columns([0.92, 1.35], gap="large")

with left:
    st.markdown('<div class="kicker">Trip brief</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="examples">
            <div class="examples-title">See some example trips</div>
            <div class="example">🗾 Plan a 7-day Japan trip with flights, hotels, and sightseeing under ₹2 lakhs</div>
            <div class="example">🗼 5 days in Paris — boutique hotels, cafés, and museum hopping</div>
            <div class="example">🌴 10-day Bali backpacking trip with beaches, temples, and a mid-range budget</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("trip_brief", clear_on_submit=False):
        st.text_area(
            "Describe the trip",
            key="trip_query",
            height=170,
            placeholder="e.g. Plan a complete 7-day Japan trip including flights, hotels and sightseeing under ₹2 lakhs",
        )
        generate = st.form_submit_button(
            "Generate plan",
            type="primary",
            use_container_width=True,
        )

    if st.session_state.form_error:
        st.warning(st.session_state.form_error)

query = (st.session_state.trip_query or "").strip()

if generate:
    if not query:
        st.session_state.form_error = "Please describe your trip first."
        st.rerun()
    st.session_state.form_error = ""

with right:
    st.markdown('<div class="kicker">Itinerary Result</div>', unsafe_allow_html=True)

    should_run = bool(generate and query)

    if should_run:
        config = {"configurable": {"thread_id": st.session_state.thread_id}}
        collected = {
            "query": query,
            "flight_results": "",
            "hotel_results": "",
            "itinerary": "",
            "final_response": "",
            "llm_calls": 0,
        }

        for chunk in app.stream(
            {
                "messages": [HumanMessage(content=query)],
                "user_query": query,
                "flight_results": "",
                "hotel_results": "",
                "itinerary": "",
                "llm_calls": 0,
            },
            config=config,
            stream_mode="updates",
        ):
            for node_name, state_update in chunk.items():
                step, label = AGENT_META.get(node_name, ("·", node_name))
                with st.status(f"{step}  {label}", state="complete", expanded=False):
                    if node_name == "flight_agent":
                        text = state_update.get("flight_results", "")
                        collected["flight_results"] = text
                        st.markdown(text or "_No flight data returned._")
                    elif node_name == "hotel_agent":
                        text = state_update.get("hotel_results", "")
                        collected["hotel_results"] = text
                        st.markdown(text or "_No hotel data returned._")
                    elif node_name == "itinerary_agent":
                        text = state_update.get("itinerary", "")
                        collected["itinerary"] = text
                        st.markdown(text or "_No itinerary generated._")
                    elif node_name == "final_agent":
                        msgs = state_update.get("messages", [])
                        text = msgs[-1].content if msgs else ""
                        collected["final_response"] = text
                        st.markdown(text or "_No final response._")
                    collected["llm_calls"] = state_update.get(
                        "llm_calls", collected["llm_calls"]
                    )

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"travel_plan_{timestamp}.md"
        save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
        os.makedirs(save_dir, exist_ok=True)
        file_content = f"""# Travel Plan
**Query:** {query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Session ID:** {st.session_state.thread_id}

---

## Flights
{collected['flight_results'] or 'N/A'}

---

## Hotels
{collected['hotel_results'] or 'N/A'}

---

## Itinerary
{collected['itinerary'] or 'N/A'}

---

## Final plan
{collected['final_response'] or 'N/A'}

---
*LLM calls: {collected['llm_calls']}*
"""
        with open(os.path.join(save_dir, filename), "w", encoding="utf-8") as f:
            f.write(file_content)

        collected["filename"] = filename
        collected["file_content"] = file_content
        st.session_state.plan = collected

    plan = st.session_state.plan
    if plan:
        st.markdown(
            f"""
            <div class="metric-row">
                <div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl">Agents</div></div>
                <div class="metric-box"><div class="metric-val">{plan['llm_calls']}</div><div class="metric-lbl">LLM calls</div></div>
                <div class="metric-box"><div class="metric-val">Done</div><div class="metric-lbl">Status</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if plan.get("final_response"):
            st.markdown(plan["final_response"])

        dl_col, info_col = st.columns([1, 2.4])
        with dl_col:
            st.download_button(
                "Download plan",
                data=plan["file_content"],
                file_name=plan["filename"],
                mime="text/markdown",
                use_container_width=True,
            )
        with info_col:
            st.markdown(
                f"<div class='save-bar'>Saved to <code>travel_plans/{plan['filename']}</code></div>",
                unsafe_allow_html=True,
            )

st.markdown(
    """
    <div class="powered">
        <div class="kicker">Powered by</div>
        <div class="powered-row">
            <span class="agent-chip">LangGraph</span>
            <span class="agent-chip">Groq · GPT-OSS 120B</span>
            <span class="agent-chip">In-memory SQLite</span>
            <span class="agent-chip">Tavily Search</span>
            <span class="agent-chip">AviationStack</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
