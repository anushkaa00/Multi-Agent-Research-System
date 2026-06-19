from dotenv import load_dotenv
load_dotenv()

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_hyperbrowser import HyperbrowserScrapeTool


#tools
search_tool = TavilySearchResults(max_results = 5) #search tool
scrape_tool = HyperbrowserScrapeTool()


