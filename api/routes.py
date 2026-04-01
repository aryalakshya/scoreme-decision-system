from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

from engine.rule_engine import RuleEngine
from services.state_manager import StateManager
from services.audit_service import AuditService
from services.idempotency_service import IdempotencyService

from services.external_service import ExternalService
from services.retry_service import RetryService

router = APIRouter()

external_service = ExternalService()
retry_service = RetryService()
rule_engine = RuleEngine()
state_manager = StateManager()
audit_service = AuditService()
idempotency_service = IdempotencyService()


class RequestModel(BaseModel):
    workflow: str
    data: Dict
    idempotency_key: str


@router.post("/process")
def process_request(request: RequestModel):

    # Idempotency check
    cached_response = idempotency_service.check(request.idempotency_key)
    if cached_response:
        return {
            "message": "Duplicate request detected",
            "cached": True,
            "response": cached_response
        }

    # Create request
    request_id = state_manager.create_request(request.data)

    # Move to processing
    state_manager.update_status(request_id, "PROCESSING")

    # Rule evaluation
    decision, rules = rule_engine.evaluate_rules(
        request.workflow,
        request.data
    )
    # If rejected early, skip external call
    if decision == "reject":
        final_decision = "reject"

    else:
        try:
            # Retry external call
            fraud_result = retry_service.execute_with_retry(
                lambda: external_service.fraud_check(request.data)
            )

            if fraud_result["fraud"]:
                final_decision = "reject"
                rules.append("fraud_check")

            else:
                final_decision = decision

        except Exception:
            final_decision = "retry"

    # Update final state
    state_manager.update_status(request_id, final_decision.upper())
    # Audit log
    audit_service.log_decision(
        request_id,
        decision,
        rules,
        request.data
    )

    response = {
        "request_id": request_id,
        "decision": final_decision,
        "rules_triggered": rules
    }

    # Store for idempotency
    idempotency_service.store(request.idempotency_key, response)

    return response