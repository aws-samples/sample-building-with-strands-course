from strands import Agent
from strands_tools import calculator, file_read, shell, http_request

agent = Agent(tools=[calculator, file_read, shell, http_request])
agent("What is the weather today in LA?")
