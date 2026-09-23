import httpx


def get_github_issue(owner: str, repo: str, issue_number: int) -> dict:
    """Fetch a GitHub issue and return the information useful for issue analysis."""

    url = (
        f"https://api.github.com/repos/"
        f"{owner}/{repo}/issues/{issue_number}"
    )

    response = httpx.get(url)

    if response.status_code != 200:
        return {
            "error": f"GitHub API request failed with status {response.status_code}"
        }

    issue = response.json()

    return {
        "number": issue["number"],
        "title": issue["title"],
        "body": issue["body"],
        "state": issue["state"],
        "author": issue["user"]["login"],
        "comments": issue["comments"],
    }