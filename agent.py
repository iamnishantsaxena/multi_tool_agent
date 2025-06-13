from google.adk.agents import Agent
from multi_tool_agent.sub.agent import (
                        greeter, 
                        weather_agent, 
                        question_answer_agent, 
                        jd_resume_coordinator_agent
                        )
from .sub.root_prompt_util import (root_agent_prompt)

root_agent = Agent(
  name="root_agent",
  model="gemini-2.0-flash-exp",
  description="Agent to manage tasks and delegate them to other agents.",
  instruction=(
      root_agent_prompt +
      # "You are a task manager agent that delegates tasks to other agents based on user queries."
      "for greetings, use the greeter agent to greet the user. do not use the greeter agent for any other tasks."
      "for weather, use the weather agent to get the current weather. "
      "for search, use the question_answer_agent agent to find information."
      "for any question, use the question_answer_agent agent to answer questions."
      "for news, use the question_answer_agent agent to get the latest news."
      "For job description or resume related tasks (including matching, analysis, or comparison), "
      "use the jd_resume_coordinator_agent which will handle the complete workflow including "
      "extraction and automatic matching when both documents are available."
  ),
  sub_agents=[
    greeter,
    question_answer_agent,
    weather_agent,
    jd_resume_coordinator_agent,
  ],
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