from datetime import datetime

class AuditService:

    def __init__(self):
        self.logs = {}

    def log_decision(self, request_id, decision, rules, data):
        self.logs[request_id] = {
            "decision": decision,
            "rules_triggered": rules,
            "input_data": data,
            "timestamp": str(datetime.utcnow())
        }

    def get_audit(self, request_id):
        return self.logs.get(request_id)