import json

class RuleEngine:

    def __init__(self, config_path="config/workflows.json"):
        with open(config_path) as f:
            self.config = json.load(f)

    def evaluate_rules(self, workflow_name, data):
        rules = self.config[workflow_name]["rules"]

        triggered_rules = []

        for rule in rules:
            field = rule["field"]
            operator = rule["operator"]
            value = rule["value"]

            if field not in data:
                return "reject", ["missing_field"]

            if not self._compare(data[field], operator, value):
                return rule["on_fail"], [rule["id"]]

            triggered_rules.append(rule["id"])

        return "approve", triggered_rules

    def _compare(self, a, operator, b):
        if operator == ">=":
            return a >= b
        elif operator == ">":
            return a > b
        elif operator == "<=":
            return a <= b
        elif operator == "<":
            return a < b
        elif operator == "==":
            return a == b
        return False