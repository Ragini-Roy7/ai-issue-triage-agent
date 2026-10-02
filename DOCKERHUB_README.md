\# AI Software Issue Triage \& Resolution Agent



A tool-using AI agent built on \*\*Google ADK\*\* and \*\*Gemini\*\* that retrieves live issue data from the \*\*GitHub REST API\*\* and analyzes it. This image packages the agent for containerized execution.



> \*\*Status:\*\* early-stage, actively developed. The current implementation covers issue retrieval and model-based analysis. It is not a production-ready service; see \[Limitations and Roadmap](#limitations-and-roadmap).



\- \*\*Docker Hub:\*\* `ragini777/ai-issue-triage-agent`

\- \*\*Source:\*\* https://github.com/Ragini-Roy7/ai-issue-triage-agent

\- \*\*Current tag:\*\* `v1`



<!-- VERIFY (remove before publishing): every statement below is derived from the GitHub README, the Docker Hub tag page, and GitHub Issue #1. Source files under my\_agent/ and the Dockerfile were not inspected. See PUBLISHING\_NOTES.md. -->



\---



\## Project Overview



\*\*Problem.\*\* Triaging a bug report starts with gathering context: the issue's content, state, labels, and surrounding project information. That retrieval step is repetitive and is a natural fit for tool-augmented LLM workflows.



\*\*What the agent does.\*\* Given a natural-language request (for example, \*"Fetch and summarize issue #1 from Ragini-Roy7/ai-issue-triage-agent"\*), the agent selects a tool through Google ADK, fetches real issue data from the GitHub REST API, and uses Gemini to analyze the result.



\*\*Intended use.\*\* A foundation for an engineering assistant that moves from bug report toward verified resolution. The current release covers the first stage only: retrieval and analysis. Later stages are roadmap items and are not implemented.



\---



\## Architecture



```mermaid

flowchart LR

&#x20;   U\[User] -->|natural-language request| UI\[ADK Web UI]

&#x20;   UI --> A\[ADK agent: my\_agent]

&#x20;   A <-->|reasoning and tool selection| G\[Gemini model]

&#x20;   A -->|tool call| T1\[GitHub issue tool]

&#x20;   A -->|tool call| T2\["get\_project\_context()"]

&#x20;   T1 -->|HTTPS request| GH\[GitHub REST API]

&#x20;   GH -->|issue data| T1

&#x20;   T1 -->|tool result| A

&#x20;   T2 -->|project context| A

&#x20;   A -->|analysis| UI

&#x20;   UI --> U

```



\*\*Request flow\*\*



1\. The user submits a request through the ADK Web interface.

2\. The ADK agent passes the request and its registered tool definitions to Gemini.

3\. Gemini decides whether a tool call is required and which tool to invoke.

4\. ADK executes the selected Python tool. The GitHub issue tool calls the GitHub REST API and returns issue data to the agent.

5\. The tool result is returned to the model, which produces the final analysis.



\*\*Components\*\*



| Layer | Role |

|---|---|

| Agent orchestration | Google ADK registers tools, manages the tool-calling loop, and serves the dev UI |

| LLM | Gemini (Flash-Lite tier) performs reasoning and tool selection |

| Tool layer | Typed Python functions exposed to the agent; one wraps GitHub REST issue retrieval |

| External API | GitHub REST API supplies live issue data |



\---



\## Current Capabilities



Implemented:



\- Tool-using agent on Google ADK, with Gemini selecting tools per request.

\- Retrieval of a single GitHub issue through the REST API: title, body, state, labels, and related metadata.

\- Model-based summarization and analysis of the retrieved issue content.

\- A `get\_project\_context()` tool that supplies project context to the agent.

\- Interactive use through the ADK Web development UI.



Known gaps in the current implementation:



\- No automated issue classification schema.

\- The final response does not yet distinguish information returned by `get\_project\_context()` from the model's own reasoning (tracked as Issue #1).



\---



\## Technology Stack



| Technology | Purpose |

|---|---|

| Python | Implementation language |

| Google ADK | Agent framework, tool registration, development UI |

| Gemini 3.5 Flash-Lite | Reasoning and tool-selection model |

| GitHub REST API | Live issue retrieval |

| ADK Web | Local development and testing interface |

| Environment variables | API key configuration |

| Docker | Container packaging |



\---



\## Containerization



Published image facts (from Docker Hub):



| Property | Value |

|---|---|

| Repository | `ragini777/ai-issue-triage-agent` |

| Tag | `v1` |

| Digest | `sha256:e23ae1ffe…` |

| Compressed size | 74 MB |



> \*\*Note:\*\* The Dockerfile is not yet committed to the GitHub repository; the `v1` image was built locally. The build instructions below assume a Dockerfile at the repository root and apply once it is committed.



<!-- VERIFY (remove before publishing): base image, WORKDIR, install steps, CMD, EXPOSE, and runtime user are NOT confirmed. Fill in a table from the real Dockerfile, or use the reference Dockerfile in PUBLISHING\_NOTES.md. -->



\*\*Design requirements for the image\*\*



\- \*\*Dependency installation:\*\* from `requirements.txt` at build time.

\- \*\*Application packaging:\*\* the `my\_agent` package is copied into the image.

\- \*\*Startup:\*\* the ADK Web server runs as the container's main process and must bind to `0.0.0.0` to be reachable through a published port.

\- \*\*Runtime port mapping:\*\* ADK Web listens on port 8000 by default; the examples below map `8000:8000`.

\- \*\*Build/runtime separation:\*\* the image holds code and dependencies only. Credentials are supplied when the container starts.



\---



\## Configuration



| Variable | Required | Purpose |

|---|---|---|

| `GEMINI\_API\_KEY` | Yes | Authenticates requests to the Gemini API |



\*\*Credential handling\*\*



Inject credentials at runtime. Do not embed them in the image, because:



\- Image layers are retained and recoverable. A key written to any layer persists even if a later layer deletes the file.

\- A published image distributes whatever its layers contain to every user who pulls it.

\- Runtime injection lets you rotate or revoke a key without rebuilding or republishing.

\- It keeps one image reusable across environments with different credentials.



Never commit `.env` files or keys to the repository, and never pass key values as literals in shell history or CI logs.



\---



\## Build and Run



All commands are PowerShell.



\*\*Clone\*\*



```powershell

git clone https://github.com/Ragini-Roy7/ai-issue-triage-agent.git

cd ai-issue-triage-agent

```



\*\*Build\*\* (requires the Dockerfile noted above)



```powershell

docker build -t ragini777/ai-issue-triage-agent:v1 .

```



\*\*Run, passing the key from your session environment\*\*



```powershell

$env:GEMINI\_API\_KEY = Read-Host "Gemini API key"

docker run -d --name issue-triage-agent -p 8000:8000 -e GEMINI\_API\_KEY ragini777/ai-issue-triage-agent:v1

```



`-e GEMINI\_API\_KEY` with no value forwards the variable from the host environment, so the key does not appear in the command line.



\*\*Run, using an env file\*\*



```powershell

docker run -d --name issue-triage-agent -p 8000:8000 --env-file .\\my\_agent\\.env ragini777/ai-issue-triage-agent:v1

```



Docker env files are read literally: use `KEY=value` lines without quotes. Keep the file out of version control and out of the build context.



Open `http://localhost:8000` and submit a request such as:



```text

Fetch and summarize issue #1 from Ragini-Roy7/ai-issue-triage-agent

```



\*\*Logs, inspection, and shutdown\*\*



```powershell

docker logs -f issue-triage-agent      # stream logs

docker ps                              # list running containers

docker inspect issue-triage-agent      # full container metadata

docker stop issue-triage-agent         # stop

docker rm issue-triage-agent           # remove

```



\---



\## Docker Hub Usage



Image reference:



```text

ragini777/ai-issue-triage-agent:v1

```



\*\*Pull and run\*\*



```powershell

docker pull ragini777/ai-issue-triage-agent:v1

$env:GEMINI\_API\_KEY = Read-Host "Gemini API key"

docker run -d --name issue-triage-agent -p 8000:8000 -e GEMINI\_API\_KEY ragini777/ai-issue-triage-agent:v1

```



\*\*Tags.\*\* A tag is a mutable pointer to an image manifest; the digest is the immutable identifier. For reproducible deployments, pin by digest:



```powershell

docker inspect --format '{{index .RepoDigests 0}}' ragini777/ai-issue-triage-agent:v1

docker pull ragini777/ai-issue-triage-agent@sha256:<digest>

```



\---



\## Security and Operational Considerations



| Area | Currently in place | Recommended hardening |

|---|---|---|

| Secret management | API key is supplied through environment variables, not source code | Inject from a secrets manager or orchestrator secret store; rotate keys; scan images for embedded secrets |

| Dependency pinning | `requirements.txt` is present; pin status not verified | Pin exact versions (preferably with hashes) and track updates |

| Build context exclusion | No `.dockerignore` in the repository | Add `.dockerignore` excluding `.env`, `.git`, virtual environments, and caches |

| Container user | Not verified | Run as a non-root user |

| Image maintenance | Single tag, `v1` | Pin the base image by digest, rebuild on a schedule, scan with Docker Scout or Trivy |

| Logging | Output readable via `docker logs` to the extent the process writes to stdout/stderr | Structured logging and log shipping |

| Health checks | None configured | Add a `HEALTHCHECK` once a suitable endpoint is defined |



The ADK Web interface is a development and testing tool. Exposing it beyond a local machine requires authentication and network controls that are not implemented.



\---



\## Limitations and Roadmap



\*\*Current limitations\*\*



\- Retrieval and analysis only; no automated classification schema.

\- Tool provenance is not surfaced in responses (Issue #1).

\- Served through the ADK development UI rather than a hardened API.

\- No evaluation suite, observability, or test coverage is documented.



\*\*Possible future extensions (none implemented)\*\*



\- Deeper issue investigation across comments and linked items

\- Repository context retrieval

\- Test generation

\- Suggested code changes

\- Human approval before any pull request is created

\- Evaluation harness and observability



\---



\## Versioning



The current image tag is `v1`. For future releases:



\- Publish immutable, specific tags (for example `v1.1.0`) and treat them as write-once.

\- Record the source commit for each tag in the release notes.

\- Avoid relying on `latest` for deployments.

\- Pin by digest where reproducibility matters.

