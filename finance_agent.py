# finance_agent.py

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

# --- New Tool: ScenarioSimulatorTool ---

class ScenarioSimulatorTool:
    """
    Tool to simulate simple "what-if" financial scenarios.
    Example: simulate revenue growth impact on EPS and P/E.
    """

    def __init__(self):
        # Initialize any internal parameters/models if needed
        pass

    def simulate_scenario(self, company_symbol: str, revenue_growth_pct: float):
        """
        Simulate a scenario where revenue grows by revenue_growth_pct.
        This example uses placeholder logic and dummy data – replace with real fetch/model.

        Args:
            company_symbol (str): Ticker symbol, e.g. 'TSLA'
            revenue_growth_pct (float): Percentage growth in revenue e.g. 15 for +15%

        Returns:
            dict: Contains markdown summary, a simple results table, (optional) charts/plots
        """

        # Dummy current financials – replace with actual data fetched via YFinanceTools or API
        dummy_financials = {
            "TSLA": {"Revenue": 80000, "EPS": 4.0, "PE": 60},
            "MSFT": {"Revenue": 143000, "EPS": 9.5, "PE": 28},
            "AAPL": {"Revenue": 365000, "EPS": 6.1, "PE": 30},
            # Add more as needed
        }

        # Get current data or default placeholders
        current = dummy_financials.get(company_symbol.upper(), None)
        if not current:
            return {
                "summary": f"Sorry, no financial data available for symbol {company_symbol}.",
                "table": None,
            }

        # Calculate projected revenue
        projected_revenue = current["Revenue"] * (1 + revenue_growth_pct / 100)

        # Very simplified EPS projection: assume EPS scales proportional to revenue growth
        projected_eps = current["EPS"] * (1 + revenue_growth_pct / 100)

        # Simplified P/E recalculation: assume price stays constant, so P/E inversely scales with EPS
        projected_pe = round(current["PE"] * (current["EPS"] / projected_eps), 2)

        # Prepare markdown-formatted summary
        summary = (
            f"**Scenario Simulation for {company_symbol.upper()}**:\n\n"
            f"- Revenue growth: {revenue_growth_pct}%\n"
            f"- Projected Revenue: ${projected_revenue:,.0f}M\n"
            f"- Projected EPS: ${projected_eps:.2f}\n"
            f"- Projected P/E ratio (price assumed stable): {projected_pe}\n\n"
            f"_Note: This is a simplified pro-forma estimate based on linear growth assumptions._"
        )

        # Prepare results table as a list of dicts or dict of lists (you can adapt to your agent's expected format)
        table = {
            "Metric": ["Current Revenue (M$)", "Projected Revenue (M$)", "Current EPS", "Projected EPS", "Current P/E", "Projected P/E"],
            "Value": [
                f"${current['Revenue']:,.0f}",
                f"${projected_revenue:,.0f}",
                f"${current['EPS']:.2f}",
                f"${projected_eps:.2f}",
                f"{current['PE']}",
                f"{projected_pe}"
            ]
        }

        # Return as dict expected by your agent
        return {
            "summary": summary,
            "table": table,
            "chart": None  # Add chart generation path or markup here if implemented
        }

    # This method enables the tool to be called by your agent infrastructure
    def __call__(self, query: str):
        """
        Parse the query to detect scenario simulation intents.
        Example query:
        "What if Tesla's revenue grows 15% next year?"
        """
        import re

        # Try to parse company symbol and growth pct from query
        pattern = r"(?:what if|simulate).*(\b[A-Z]{1,5}\b|Tesla|Microsoft|Apple|MSFT|TSLA|AAPL)[^\d]*(\d{1,3})\s*%"

        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            company = match.group(1).upper()
            growth_pct = float(match.group(2))

            # Run simulation
            result = self.simulate_scenario(company, growth_pct)
            return result

        # If no match, return None to indicate no action
        return None


# --- Existing finance_agent definition with new tool added ---

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data and run scenario simulations",
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[
        YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True),
        ScenarioSimulatorTool(),  # <-- Newly added scenario simulation tool
    ],
    instructions=[
        "Use tables to display data.",
        "Use ScenarioSimulatorTool for forecasting scenarios and 'what-if' revenue growth queries.",
    ],
    show_tool_calls=True,
    markdown=True,
)
