from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.sub.agent import (
    jd_extractor_agent,
    resume_extractor_agent,
    resume_jd_matcher_agent
)
from .sub.root_prompt_util import (root_agent_prompt)

root_agent = Agent(
    name="root_agent",
    description=(
      "Root agent that coordinates multiple sub-agents for job description and resume processing. "
      "It can extract job descriptions, extract resumes, and automatically performs matching and summarization when both documents are available."
    ),
    model="gemini-2.0-flash-exp",
    instruction=root_agent_prompt,
    tools=[
        AgentTool(agent=jd_extractor_agent),
        AgentTool(agent=resume_extractor_agent),
        AgentTool(agent=resume_jd_matcher_agent)
    ],
    output_key="match_result",
    # show_tool_calls=False,
)

agent = root_agent

# Sample prompts for testing each agent
# 1. Weather Agent
# Whats the weather like in New York?
# 2. Question and Answer Agent
# What is the capital of France?
# 3. News Agent
# Latest updates on artificial intelligence
# 4. JD Extractor Agent
# Extract job description from the text: "We are seeking a Python developer with experience in Django and REST APIs."
# 5. Resume Extractor Agent
# Extract resume information from the text: "Jane Doe is a software engineer skilled in Python, Django, and REST APIs."
# 6. Resume JD Matcher Agent
# Match the resume with the job description: "Jane Doe has 3 years of experience with Python and Django.", "Looking for a Python developer with Django experience."
# 7. Resume JD Matcher Summariser Agent
# Summarise the match result: "The candidate has relevant Python and Django experience matching the job requirements."