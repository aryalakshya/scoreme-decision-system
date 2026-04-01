# ScoreMe Decision System

## Overview
This project implements a configurable workflow decision platform that processes business requests using rule evaluation, workflow execution, and state tracking.

The system is designed to handle real-world challenges such as failures, retries, idempotency, and auditability.

---

## Highlights
- Config-driven workflow engine (no hardcoded logic)
- Idempotency to prevent duplicate processing
- Retry mechanism with exponential backoff for external failures
- Audit logging for explainable decision-making
- Modular and extensible architecture
- Test coverage for core scenarios

---

## Features
- Configurable workflows via JSON
- Rule-based decision engine
- State lifecycle tracking
- Idempotency support (duplicate request handling)
- External dependency simulation with retry logic
- Audit logs for explainability
- REST API built using FastAPI
- Test coverage using Pytest

---

## Multi-Workflow Support

The system supports multiple workflows via configuration.

Example workflows implemented:
- Loan Approval
- Employee Onboarding
- Claim Processing
- Vendor Approval

New workflows can be added by updating `workflows.json` without modifying code.

---

## System Architecture
The system is divided into modular components:

- API Layer (FastAPI)
- Rule Engine
- Workflow Engine
- State Manager
- Audit Service
- Idempotency Service
- External Service Simulator

For detailed design, refer to `architecture.md`.

---

## Project Structure
scoreme-decision-system/<br>
│<br>
├── api/<br>
├── config/<br>
├── db/<br>
├── engine/<br>
├── services/<br>
├── tests/<br>
│<br>
├── main.py<br>
├── README.md<br>
├── architecture.md<br>
├── requirements.txt<br>
├── .gitignore<br>


---

## How to Run

### 1. Clone the repository
```bash
git clone "https://github.com/aryalakshya/scoreme-decision-system"
cd scoreme-decision-system


### 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

### 3. Install dependencies 
pip install -r requirements.txt

### 4. Run the server
uvicorn main:app --reload

###5. Open API docs
http://127.0.0.1:8000/docs

#Example Request:
{
  "workflow": "loan_approval",
  "data": {
    "age": 25,
    "credit_score": 650
  },
  "idempotency_key": "abc123"
}

##Running tests:
pytest


##Key Engineering Decisions
Config-driven workflows for flexibility
Separation of concerns for modularity
Idempotency to prevent duplicate execution
Retry logic for resilience against failures
Audit logging for explainability and debugging


##Trade-offs
In-memory storage used instead of database for simplicity
External dependency is simulated
Retry logic is basic (can be extended)


##Future Improvements
PostgreSQL integration for persistence
Redis for caching and idempotency
Message queues for async workflows
LLM-based decision explanations
UI dashboard for monitoring