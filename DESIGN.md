\# VulnVerdict – System Design



\## 1. Project Overview



VulnVerdict is a security and regulatory intelligence application designed to help small SaaS companies understand security vulnerabilities and CERT-In advisories affecting their software products.



The application uses a Large Language Model (LLM) to generate responses to user queries. It also tracks token consumption and estimates API usage costs.



\## 2. Technology Stack



\- \*\*Backend:\*\* Python, FastAPI

\- \*\*LLM Integration:\*\* Google Gemini API

\- \*\*Database:\*\* SQLite

\- \*\*Validation:\*\* Pydantic

\- \*\*Testing:\*\* Pytest

\- \*\*Code Quality:\*\* Ruff

\- \*\*Containerization:\*\* Docker

\- \*\*CI/CD:\*\* GitHub Actions



\## 3. System Architecture



The application follows a layered architecture:



1\. Client sends an HTTP request.

2\. FastAPI receives and validates the request.

3\. The LLM service sends the prompt to the configured Gemini model.

4\. If the primary model fails, the service attempts the fallback model.

5\. The response and token usage information are collected.

6\. The usage service stores token consumption and estimated cost in SQLite.

7\. FastAPI returns the generated response to the client.



\## 4. API Endpoints



\### GET /health



Purpose: Checks whether the application is running.



Response:

\- status

\- app

\- environment



\### POST /generate



Purpose: Generates an answer using the configured Gemini model.



Request:

\- prompt



Response:

\- answer

\- model

\- prompt\_tokens

\- response\_tokens

\- total\_tokens



The service attempts the fallback model if the primary model fails.



\### GET /usage



Purpose: Returns aggregated LLM usage statistics.



Response:

\- total\_requests

\- total\_prompt\_tokens

\- total\_response\_tokens

\- total\_thoughts\_tokens

\- total\_tokens

\- estimated\_cost\_usd



\## 5. Database Design



The application uses SQLite to persist LLM usage information.



\### Table: usage\_logs



| Column | Description |

|---|---|

| id | Unique usage record ID |

| model | Gemini model used |

| prompt\_tokens | Input tokens consumed |

| response\_tokens | Output tokens generated |

| thoughts\_tokens | Thinking tokens reported by the model |

| total\_tokens | Total tokens reported |

| estimated\_cost\_usd | Estimated API cost |

| created\_at | Record creation timestamp |



Each successful generation request creates a usage record.



\## 6. LLM Fallback Mechanism



The application is configured with:

\- Primary model: gemini-3.5-flash

\- Fallback model: gemini-3.7-flash



The LLM service first attempts to generate a response using the primary model.



If that request fails, it attempts the fallback model. If both models fail, the API returns an HTTP 502 error.



\## 7. Token and Cost Tracking



For every successful generation request, the application collects token usage metadata from the Gemini API.



The usage service stores:

\- Input tokens

\- Output tokens

\- Thinking tokens

\- Total tokens

\- Estimated API cost



The cost is an estimate based on configured model pricing, not the actual billed amount.



\## 8. Testing and Continuous Integration



The project uses:

\- Ruff for code quality checks.

\- Pytest for automated testing.

\- GitHub Actions to run checks on pushes and pull requests.



The CI workflow installs dependencies, runs Ruff, and executes the test suite.



\## 9. Deployment



The application is containerized using Docker.



The Docker image runs the FastAPI application and exposes its API endpoints. The Gemini API key is supplied through an environment variable and is not committed to the Git repository.
