from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .prompt import (
    jd_entity_extraction_prompt,
    resume_extractor_prompt,
    resume_jd_matcher_prompt,
)
from .util_resumeExtractor import ResumeExtractorTool
from multi_tool_agent.dtypes_common import CandidateResume, JobDescription  # Import Pydantic models
import json

resume_file_extractor_tool = ResumeExtractorTool()

def create_extraction_agent(name, description, instruction, model="gemini-2.0-flash-exp", tool=None):
    tools = [tool] if tool else []
    return Agent(
        name=name,
        description=description,
        model=model,
        instruction=instruction,
        tools=tools
    )

# Define the agents for resume and job description extraction, and matching
resume_extractor_agent = create_extraction_agent(
    name="resume_extractor_agent",
    description="The agent that extracts and structures resume information from text",
    instruction=resume_extractor_prompt,
    tool=resume_file_extractor_tool
)

jd_extractor_agent = create_extraction_agent(
    name="jd_extractor_agent",
    description="The agent that extracts and structures job description information from text",
    instruction=jd_entity_extraction_prompt
)

resume_jd_matcher_agent = Agent(
    name="resume_jd_matcher_agent",
    description=(
        "The agent that summarises the match result between the job description and the resume. "
        "It takes the match result as input and provides a summary of the match."
    ),
    model="gemini-2.0-flash-exp",
    instruction=resume_jd_matcher_prompt,
    output_key="match_result"
)