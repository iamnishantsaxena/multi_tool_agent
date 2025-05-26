from google.adk.agents import Agent
from google.adk.tools import google_search

from .weather_util import get_weather
from .time_util import get_current_time
from .jd_prompt import (
    jd_entity_extraction_prompt,
    resume_extractor_prompt,
    resume_jd_matcher_prompt,
    resume_jd_matcher_summariser_prompt
)
from .root_prompt import (root_agent_prompt)
  

# Create an instance of the LlmAgent for Weather and Time
weather_agent = Agent(
    name="weather_agent",
    model="gemini-2.0-flash-exp",
    description=(
      "Agent to answer questions about the weather and time in a city."
    ),
    instruction=(
      "You are a helpful agent who can answer user questions about the weather and time in a city."
    ),
    tools=[get_weather, get_current_time],
)

question_answer_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="question_answer_agent",
    description="A helpful assistant agent that can answer questions.",
    instruction="""Respond to the query using google search.""",
    tools=[google_search],
)

# Create an instance of the LlmAgent for JD and Resume
jd_extractor_agent = Agent(
    name="jd_extractor_agent",
    description="The agent that extracts the job description from the text",
    model="gemini-2.0-flash-exp",
    instruction=jd_entity_extraction_prompt,
    output_key="job_description"
)

resume_extractor_agent = Agent(
    name="resume_extractor_agent",
    description="The agent that extracts the resume from the text",
    model="gemini-2.0-flash-exp",
    instruction=resume_extractor_prompt,
    output_key="candidate_resume"
)

resume_jd_matcher_agent = Agent(
    name="jd_to_resume_matcher_agent",
    description="The agent that matches the job description to the resume",
    model="gemini-2.0-flash-exp",
    instruction=resume_jd_matcher_prompt,
    output_key="match_result"
)

resume_jd_matcher_summariser_agent = Agent(
    name="jd_matcher_summariser_agent",
    description="The agent that summarises the match result",
    model="gemini-2.0-flash-exp",
    instruction=resume_jd_matcher_summariser_prompt,
    output_key="summary"
)

# Create an instance of the LlmAgent for JD and Resume

jd_resume_agent = Agent(
    name="jd_resume_agent",
    model="gemini-2.0-flash-exp",
    description="Agent to manage job description and resume tasks.",
    instruction=(root_agent_prompt),
    sub_agents=[
        jd_extractor_agent,
        resume_extractor_agent,
        resume_jd_matcher_agent,
        resume_jd_matcher_summariser_agent
    ],
)

greeter = Agent(
    name="greeter",
    model="gemini-2.0-flash-exp",  # Required: Specify the LLM
    description="A simple agent that greets the user.",
    instruction = (
      root_agent_prompt +
      "You are a friendly agent that greets the user warmly. "
      "do not respond to any other queries, just greet the user."
      ),
    output_key="greeting",
    tools=[weather_agent, jd_resume_agent, question_answer_agent] 
)