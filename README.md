Finsage AI
Finsage AI is a powerful AI-driven multi-agent system designed to assist retail investors, analysts, and financial enthusiasts in making smarter investment decisions. Built with Python, LLAMA 3.1 (8B Instant), Phidata, and real-time data sources, Finsage AI brings together financial intelligence, data orchestration, and advanced language models in one seamless platform.

🚀 Features
📈 Real-time stock market insights and analytics

🧠 Multi-agent architecture using phidata for coordinated financial tasks

🤖 Built-in LLM agents with Llama 3.1 (8B Instant) for intelligent financial reasoning

📊 Market Sentiment Analysis

📰 Live News Fetching and Analysis

🛠️ Extensible framework to add custom financial tools or agents

🛠️ Tech Stack
Python

Phidata

Llama 3.1 (GroqCloud API)

Finnhub / NewsAPI / OpenAI / Any other API as per use

LangChain, Pandas, Matplotlib (for data processing and visualization)

🔐 Environment Setup
Before running the project, create a .env file in the root directory and store your own API keys as shown below:

bash
Copy
Edit
# .env
GROQ_API_KEY=your_groq_api_key
OPENAI_API_KEY=your_openai_api_key
FINNHUB_API_KEY=your_finnhub_api_key
NEWS_API_KEY=your_news_api_key
🧪 Installation
bash
Copy
Edit
git clone https://github.com/your-username/FinsageAI.git
cd FinsageAI
pip install -r requirements.txt
▶️ Running the App
bash
Copy
Edit
phidata app run
This will launch the Finsage AI agent system where you can interact with the assistant to get stock insights, financial news summaries, and more.
