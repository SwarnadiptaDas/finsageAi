from phi.agent import Agent, Tool
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

# -----------------------
# Define your sub-agents
# -----------------------

web_agent = Agent(
    name="Web Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)

# -----------------------
# Task transfer functions
# -----------------------

def transfer_task_to_finance_agent(task_description, expected_output=None, additional_information=None):
    """
    Forward a task to the finance_agent and return its response.
    """
    prompt = task_description
    if additional_information:
        prompt += "\nAdditional information: " + additional_information
    return finance_agent.print_response(prompt, stream=False)


def transfer_task_to_web_agent(task_description, expected_output=None, additional_information=None):
    """
    Forward a task to the web_agent and return its response.
    """
    prompt = task_description
    if additional_information:
        prompt += "\nAdditional information: " + additional_information
    return web_agent.print_response(prompt, stream=False)


# -----------------------
# Wrap transfer functions as Tools (with type + function schema)
# -----------------------

transfer_to_finance_tool = Tool(
    name="transfer_task_to_finance_agent",
    func=transfer_task_to_finance_agent,
    type="function",  # required for schema
    function={
        "name": "transfer_task_to_finance_agent",
        "description": "Forward a query to the finance agent for financial data and analysis.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_description": {"type": "string", "description": "The query or instruction to pass to the finance agent"},
                "expected_output": {"type": ["string", "null"], "description": "Optional expected output format"},
                "additional_information": {"type": ["string", "null"], "description": "Any extra context or requirements"}
            },
            "required": ["task_description"]
        }
    }
)

transfer_to_web_tool = Tool(
    name="transfer_task_to_web_agent",
    func=transfer_task_to_web_agent,
    type="function",  # required for schema
    function={
        "name": "transfer_task_to_web_agent",
        "description": "Forward a query to the web agent for web search and latest news.",
        "parameters": {
            "type": "object",
            "properties": {
                "task_description": {"type": "string", "description": "The query or instruction to pass to the web agent"},
                "expected_output": {"type": ["string", "null"], "description": "Optional expected output format"},
                "additional_information": {"type": ["string", "null"], "description": "Any extra context or requirements"}
            },
            "required": ["task_description"]
        }
    }
)


# -----------------------
# Define the multi-agent Team Agent
# -----------------------

agent_team = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    team=[web_agent, finance_agent],
    tools=[transfer_to_finance_tool, transfer_to_web_tool],  # important
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,
    markdown=True,
)


# -----------------------
# Run directly for testing
# -----------------------

if __name__ == "__main__":
    query = "Summarize analyst recommendations and share the latest news for NVDA"
    response = agent_team.print_response(query, stream=False)
    print(response)
