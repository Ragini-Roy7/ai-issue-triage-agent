from google.adk.agents.llm_agent import Agent
from my_agent.tools.github import get_github_issue

def get_project_context() -> str:
    """Returns important context about the AI issue triage project."""
    return """
    Project: AI Software Issue Triage & Resolution Agent

    Purpose:
    Analyze software engineering issues and help developers investigate,
    diagnose, fix, test, and document issues.

    Current stage:
    Version 1 - Tool-using agent.

    Planned capabilities:
    - GitHub issue analysis
    - Repository investigation
    - Root-cause analysis
    - Fix generation
    - Automated test generation
    - Sandboxed verification
    - Human approval for risky actions
    """


root_agent = Agent(
    model='gemini-3.5-flash-lite',
    name='root_agent',
    description='An AI agent that assists with software issue triage and investigation.',
    instruction="""
    You are an AI software issue triage assistant.

    Help developers understand and investigate software issues.

    When you need information about the project itself, use the
    get_project_context tool instead of guessing.
    
    When the user asks you to inspect a GitHub issue, use the
get_github_issue tool to retrieve the issue before analyzing it.
    """,
    tools=[get_project_context, get_github_issue],
)