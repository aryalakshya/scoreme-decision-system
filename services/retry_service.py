import time

class RetryService:

    def execute_with_retry(self, func, retries=3):

        for attempt in range(retries):
            try:
                return func()
            except Exception as e:
                print(f"Retry {attempt+1} failed: {e}")
                time.sleep(2 ** attempt)

        raise Exception("All retries failed")