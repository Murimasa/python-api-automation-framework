[![API Regression Suite](https://github.com/Mur1masa/python-api-automation-framework/actions/workflows/tests.yml/badge.svg)](https://github.com/Mur1masa/python-api-automation-framework/actions/workflows/tests.yml)
# Enterprise Python API Automation Framework

Scalable, production-ready API testing framework designed for regression and contract testing of RESTful microservices.

## Key Architectural Features

* **Custom HTTP Client Layer (`core/api_client.py`):** Encapsulates HTTP sessions, base URL routing, bearer authentication, and automatic Allure payload/response attachments.
* **Contract Validation (`pydantic`):** Enforces rigid schema parsing, payload types, and response structure compliance.
* **Dynamic Data Generation (`faker`):** Data factories prevent test data collision and enable state isolation.
* **Lifecycle Management:** Dedicated setup/teardown fixtures (`pytest` + `yield`) guarantee isolated test state and backend cleanup.
* **Parallel Execution (`pytest-xdist`):** Multi-threaded execution across isolated worker nodes.
* **Data-Driven Testing:** Granular negative boundary matrices leveraging `@pytest.mark.parametrize`.
* **CI/CD Integration:** Fully automated execution pipeline via GitHub Actions.

## Tech Stack

* **Language:** Python 3.12+
* **Test Runner:** `pytest`, `pytest-xdist`
* **HTTP Client:** `requests`
* **Schema Validation:** `pydantic`
* **Data Generation:** `Faker`
* **Reporting:** `allure-pytest`
* **Environment:** `python-dotenv`

## Project Structure

```text
├── .github/workflows/     # CI/CD automation pipelines
├── core/                  # Core framework modules (ApiClient, Data Factories)
├── tests/                 # Functional, contract, and lifecycle test suites
├── .env                   # Local environment configuration (git-ignored)
├── .gitignore             # Git exclusion rules
├── conftest.py            # Global fixtures and session lifecycle
├── pytest.ini             # Pytest runtime configuration
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation