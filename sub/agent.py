from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .prompt import (
    jd_entity_extraction_prompt,
    resume_extractor_prompt,
    resume_jd_matcher_helper_prompt,
    resume_jd_matcher_prompt,
    # jd_resume_coordinator_prompt
)

# Individual extraction agents (used as tools)
jd_extractor_agent = Agent(
    name="jd_extractor_agent",
    description="The agent that extracts and structures job description information from text",
    model="gemini-2.0-flash-exp",
    instruction=jd_entity_extraction_prompt,
)

resume_extractor_agent = Agent(
    name="resume_extractor_agent",
    description="The agent that extracts and structures resume information from text",
    model="gemini-2.0-flash-exp",
    instruction=resume_extractor_prompt,
)

resume_jd_matcher_helper_agent = Agent(
    name="resume_jd_matcher_helper_agent",
    description="The agent that matches the job description to the resume",
    model="gemini-2.0-flash-exp",
    instruction=resume_jd_matcher_helper_prompt,
)

resume_jd_matcher_agent = Agent(
    name="resume_jd_matcher_agent",
    description=(
        "The agent that summarises the match result between the job description and the resume. "
        "It takes the match result as input and provides a summary of the match."
    ),
    model="gemini-2.0-flash-exp",
    instruction=resume_jd_matcher_prompt,
    tools=[AgentTool(agent=resume_jd_matcher_helper_agent)],
    output_key="match_result",
    # show_tool_calls=False,
)

# # NEW: Coordinator Agent that manages the entire JD-Resume workflow
# jd_resume_coordinator_agent = Agent(
#     name="jd_resume_coordinator_agent",
#     description=(
#       "Coordinator agent that handles all job description and resume related tasks."
#       "It can extract job descriptions, extract resumes, and automatically performs matching and summarization when both documents are available."
#     ),
#     model="gemini-2.0-flash-exp",
#     instruction=jd_resume_coordinator_prompt,
#     tools=[
#         AgentTool(agent=jd_extractor_agent),
#         AgentTool(agent=resume_extractor_agent),
#         AgentTool(agent=resume_jd_matcher_summariser_agent)
#     ],
#     output_key="final_result",
#     # show_tool_calls=False,
# )