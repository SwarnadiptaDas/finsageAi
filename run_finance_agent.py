from agent_team import finance_agent

response = finance_agent.print_response(
    "What if Tesla's revenue grows 15% next year?", stream=False
)
print(response)
