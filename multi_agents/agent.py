from google.adk.agents import Agent
from google.adk.tools import google_search
from .sub.agents import weather_agent, search_agent, news_agent, jd_extractor_agent, resume_extractor_agent, resume_jd_matcher_agent, resume_jd_matcher_summariser_agent
from .sub.prompt_util import (root_agent_prompt)

# Create an instance of the LlmAgent for the root agent
root_agent = Agent(
    name="root_agent",
    model="gemini-2.0-flash-exp",
    description=(
      "Agent to delegate tasks to other agents based on user queries."
    ),
    instruction=(
      root_agent_prompt
    ),
    sub_agents=[search_agent, 
                weather_agent, 
                news_agent,
                ],
)