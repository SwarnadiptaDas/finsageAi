# run_agent_team.py

from agent_team import agent_team

def main():
    query = "Summarize analyst recommendations and share the latest news for NVDA"
    response = agent_team.print_response(query, stream=False)
    print(response)

if __name__ == "__main__":
    main()

