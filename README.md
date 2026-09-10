# AI Travel Planning System using LangGraph

This project is a Real-World Multi-Agent AI System built using LangGraph.

The system uses 4 AI agents that work together to plan a complete trip automatically.

## Features

- ✈️ Flight Search Agent
- 🏨 Hotel Search Agent
- 🗓️ Itinerary Planning Agent
- 🤖 Final Response Agent
- 🧠 Memory using in-memory SQLite
- 🌐 Real-time API Integration
- 💻 Streamlit Web Interface

---

# Tech Stack

- LangGraph
- LangChain
- Groq
- Groq (GPT-OSS 120B)
- SQLite (in-memory)
- Streamlit
- Tavily API
- AviationStack API

---

# Step 1: Create an Isolated Python Environment

Python 3.11–3.13 is recommended. From the project folder:

```bash
python3.13 -m venv .venv
```

If `python3.13` is not available, use `python3` instead:

```bash
python3 -m venv .venv
```

Activate the environment:

#### macOS / Linux

```bash
source .venv/bin/activate
```

#### Windows

```bash
.venv\Scripts\activate
```

You should see `(.venv)` in your terminal prompt after activation.

---

# Step 2: Install Dependencies

With the virtual environment activated:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Conversation memory is stored in an in-memory SQLite database. No separate database install is required. Memory lasts for the lifetime of the running process.

---

# Step 3: Setup `.env` File

Copy `.env.example` to `.env` inside the project folder and fill in your keys:

```bash
cp .env.example .env
```

```
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=openai/gpt-oss-120b
TAVILY_API_KEY=your_tavily_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
```

---

# Step 4: Get API Keys

## Get Groq API Key

https://console.groq.com

---

## Get Tavily API Key

https://tavily.com

---

## Get AviationStack API Key

https://aviationstack.com

---

# Step 5: Run the Application

Keep the virtual environment activated.

#### Run Multi-Agent System in Terminal

```bash
python main.py
```

This will test the multi-agent system through the terminal.

---

#### Run Streamlit Web App

```bash
streamlit run frontend.py
```

This will launch the Multi-Agent AI web application.

---

# Deploy on Streamlit Community Cloud

1. Push the repo to GitHub (do not commit `.env`).
2. At [share.streamlit.io](https://share.streamlit.io), deploy the repo.
3. Set **Main file path** to `streamlit_app.py` (or `frontend.py`). Do **not** use `main.py` — that is the terminal CLI and will show a blank page.
4. In **Advanced settings**, set Python to **3.12**.
5. Add secrets: `GROQ_API_KEY`, `GROQ_MODEL`, `TAVILY_API_KEY`, `AVIATIONSTACK_API_KEY`.
6. Reboot the app.

---

#### Example Prompt

Plan a complete 7 days Japan trip including flights, hotels and sightseeing under 2 lakhs.

---

# Project Workflow

1. Flight Agent searches flights
2. Hotel Agent searches hotels
3. Itinerary Agent creates travel plan
4. Final Agent combines everything together
5. In-memory SQLite stores conversation memory for the current process
