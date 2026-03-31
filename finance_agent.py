from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv
import re

load_dotenv()

# -----------------------
# Scenario Simulator Tool
# -----------------------

class ScenarioSimulatorTool:
    def simulate_scenario(self, company_symbol: str, growth: float):

        dummy = {
            "TSLA": {"Revenue": 80000, "EPS": 4.0, "PE": 60},
            "AAPL": {"Revenue": 365000, "EPS": 6.1, "PE": 30},
            "MSFT": {"Revenue": 143000, "EPS": 9.5, "PE": 28},
        }

        data = dummy.get(company_symbol, None)
        if not data:
            return f"No data available for {company_symbol}"

        new_rev = data["Revenue"] * (1 + growth / 100)
        new_eps = data["EPS"] * (1 + growth / 100)
        new_pe = round(data["PE"] * (data["EPS"] / new_eps), 2)

        return f"""
### Scenario Simulation for {company_symbol}

- Revenue Growth: {growth}%
- Projected Revenue: ${new_rev:,.0f}M
- Projected EPS: ${new_eps:.2f}
- Projected P/E: {new_pe}
"""

    def __call__(self, query: str):
        pattern = r"(tesla|tsla|apple|aapl|microsoft|msft).*?(\d{1,3})\s*%"
        match = re.search(pattern, query.lower())

        if match:
            company = match.group(1).upper()
            mapping = {"TESLA": "TSLA", "APPLE": "AAPL", "MICROSOFT": "MSFT"}
            company = mapping.get(company, company)

            growth = float(match.group(2))
            return self.simulate_scenario(company, growth)

        return None


# -----------------------
# Finance Agent
# -----------------------

finance_agent = Agent(
    name="Finance Agent",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        ScenarioSimulatorTool(),
        YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True),
    ],
    instructions=[
        "Handle stock queries, investments, and financial analysis.",
        "Use ScenarioSimulatorTool for growth simulations.",
        "Use tables where helpful."
    ],
    markdown=True,
)
