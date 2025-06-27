from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from multi_tool_agent.sub.agent import (
    jd_extractor_agent,
    resume_extractor_agent,
    resume_jd_matcher_agent
)
from .sub.root_prompt import (root_prompt)

root_agent = Agent(
    name="root_agent",
    description=(
      "Root agent that coordinates multiple sub-agents for job description and resume processing. "
      "It can extract job descriptions, extract resumes, and automatically performs matching and summarization when both documents are available."
    ),
    # model="gemini-2.0-flash-exp",
    model="gemini-1.5-pro-latest",
    instruction=root_prompt,
    tools=[
        AgentTool(agent=jd_extractor_agent),
        AgentTool(agent=resume_extractor_agent),
        AgentTool(agent=resume_jd_matcher_agent)
    ],
    output_key="match_result",
    # show_tool_calls=False,
)

agent = root_agent
