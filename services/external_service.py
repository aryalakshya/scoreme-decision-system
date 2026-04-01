import random
import time

class ExternalService:

    def fraud_check(self, data):
        # Simulate delay
        time.sleep(1)

        # 30% chance of failure
        if random.random() < 0.3:
            raise Exception("Fraud service unavailable")

        # Simulate fraud result
        if data.get("credit_score", 0) < 600:
            return {"fraud": True}

        return {"fraud": False}