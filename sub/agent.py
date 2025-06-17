from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompt import (
    jd_entity_extraction_prompt,
    resume_extractor_prompt,
    resume_jd_matcher_helper_prompt,
    resume_jd_matcher_prompt,
)
from .util_resumeExtractor import ResumeExtractorTool


resume_file_extractor_tool = ResumeExtractorTool()

# Define the agents for resume and job description extraction, and matching
resume_extractor_agent = Agent(
    name="resume_extractor_agent",
    description="The agent that extracts and structures resume information from text",
    model="gemini-2.0-flash-exp",
    instruction=resume_extractor_prompt,
    tools=[resume_file_extractor_tool],
)

jd_extractor_agent = Agent(
    name="jd_extractor_agent",
    description="The agent that extracts and structures job description information from text",
    model="gemini-2.0-flash-exp",
    instruction=jd_entity_extraction_prompt,
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
    # tools=[AgentTool(agent=resume_jd_matcher_helper_agent)], # Removed AgentTool
    output_key="match_result",
    # show_tool_calls=False,
)