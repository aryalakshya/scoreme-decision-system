import uuid
from datetime import datetime

class StateManager:

    def __init__(self):
        # In-memory DB (we'll replace later with real DB)
        self.store = {}

    def create_request(self, data):
        request_id = str(uuid.uuid4())

        self.store[request_id] = {
            "status": "RECEIVED",
            "data": data,
            "history": [
                {
                    "status": "RECEIVED",
                    "timestamp": str(datetime.utcnow())
                }
            ]
        }

        return request_id

    def update_status(self, request_id, new_status):
        self.store[request_id]["status"] = new_status
        self.store[request_id]["history"].append({
            "status": new_status,
            "timestamp": str(datetime.utcnow())
        })

    def get_request(self, request_id):
        return self.store.get(request_id)