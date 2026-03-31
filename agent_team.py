from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv

from finance_agent import finance_agent

load_dotenv()

# -----------------------
# Web Agent
# -----------------------

web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    markdown=True
)

# -----------------------
# Smart Router Agent
# -----------------------

router_agent = Agent(
    name="Router",
    model=Groq(id="llama-3.3-70b-versatile"),
    instructions=[
        "Classify the query.",
        "If finance-related → FINANCE",
        "Else → GENERAL",
        "Only output one word."
    ]
)

# -----------------------
# MAIN ROUTER FUNCTION
# -----------------------

def run_agent(query: str):
    try:
        decision = router_agent.run(query).content.strip().upper()

        if "FINANCE" in decision:
            return finance_agent.run(query).content
        else:
            return web_agent.run(query).content

    except Exception:
        return finance_agent.run(query).content
