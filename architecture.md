# Architecture Document - ScoreMe Decision System

## 1. Overview

This system is a configurable workflow decision platform designed to process business requests through rule evaluation, workflow execution, and state tracking.

It is built to handle real-world constraints such as failures, retries, idempotency, and auditability.

---

## 2. System Components

### 1. API Layer (FastAPI)
- Accepts incoming requests
- Validates schema using Pydantic
- Routes requests to processing engine

### 2. Rule Engine
- Evaluates configurable rules from JSON
- Supports threshold checks and mandatory validations
- Determines initial decision (approve/reject/manual_review)

### 3. Workflow Execution Layer
- Orchestrates multi-step decision process
- Integrates rule evaluation and external services

### 4. State Manager
- Maintains request lifecycle
- Tracks status transitions:
  RECEIVED → PROCESSING → FINAL STATE
- Stores history for traceability

### 5. Audit Service
- Logs:
  - Decision taken
  - Rules triggered
  - Input data used
- Enables explainability and debugging

### 6. Idempotency Service
- Prevents duplicate request processing
- Returns cached response for repeated requests

### 7. External Service Simulator
- Simulates dependency (e.g., fraud check API)
- Introduces random failures to mimic real-world systems

### 8. Retry Mechanism
- Implements exponential backoff
- Ensures resilience against transient failures

---

## 3. Data Flow

Request → API → State Manager (RECEIVED)  
→ Rule Engine → External Service → Retry Logic  
→ Decision → State Update → Audit Log → Response

---

## 4. Key Design Decisions

- **Config-driven workflows**: Allows easy modification without code changes
- **Separation of concerns**: Improves modularity and maintainability
- **Idempotency support**: Prevents duplicate processing
- **Retry logic**: Handles transient failures gracefully
- **Audit logging**: Enables explainability

---

## 5. Trade-offs

- Used in-memory storage instead of database for simplicity
- External service is simulated rather than real API
- Retry logic is basic (can be enhanced with circuit breakers)

---

## 6. Scalability Considerations

- Stateless API allows horizontal scaling
- Can integrate Redis for caching/idempotency
- Message queues (Kafka/RabbitMQ) can handle async workflows
- Database (PostgreSQL) can replace in-memory storage

---

## 7. Future Improvements

- Persistent database integration
- UI dashboard for workflow visualization
- LLM-based explanation engine
- Advanced rule engine (DSL-based rules)