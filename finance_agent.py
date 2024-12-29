from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo

import os
from dotenv import load_dotenv

load_dotenv()

os.environ["PHI_DATA_API_KEY"] = os.getenv("PHI_DATA_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

web_agent = Agent(
    name = 'web_agent',
    role = 'searching the web',
    model = Groq(id = 'llama3-groq-70b-8192-tool-use-preview'),
    tools = [DuckDuckGo()],
    instructions = ['always include source of the information'],
    show_tool_calls=True,
    markdown=True
)

yfin_agent = Agent(
    name = 'ifin_agent',
    role = 'searching the yfinance API',
    model = Groq(id = 'llama3-groq-70b-8192-tool-use-preview'),
    tools = [YFinanceTools(stock_price=True, stock_fundamentals=True, analyst_recommendations=True, company_news=True)],
    instructions = ['use table format to provide the information'],
    show_tool_calls=True,
    markdown=True
)

multi_agent = Agent(
    team=[web_agent, yfin_agent],
    instructions=['always include the source of the information and use table format to display the data'],
    show_tool_calls=True,
    markdown=True
)

multi_agent.print_response('give me the insights on CDSL based on the data you can extract', stream=True)