from services.TestCycleService.TestCycleService import TestCycleService
from services.TestCaseService.TestCaseService import TestCaseService
from models.TestCase.TestCaseDao import TestCaseDAO

"""
FastMCP quickstart example.

cd to the `examples/snippets/clients` directory and run:
    uv run server fastmcp_quickstart stdio
"""

from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


@mcp.tool()
def get_testcycle(keyorid):
    trs = TestCycleService()
    return trs.get_test_cycle(keyorid)


@mcp.tool()
def create_test_case_with_steps(
    project_id: int, summary: str, description: str = "", steps: list = None
) -> dict:
    """Create a new test case with test steps

    Args:
        project_id: The Jira project ID where the test case will be created
        summary: Brief summary of the test case
        description: Detailed description of the test case (optional)
        steps: List of test steps, each containing stepDetails, expectedResult, and testData

    Returns:
        Dict containing the created test case data
    """
    dao = TestCaseDAO()
    service = TestCaseService(dao)

    return service.create_new_test_case(
        project_id=project_id, summary=summary, description=description, steps=steps
    )


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


if __name__ == "__main__":
    mcp.run()
