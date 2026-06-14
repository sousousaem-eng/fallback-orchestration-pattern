"""
Resilient Service Orchestrator
Pattern: Failover and Observability in Distributed Service Requests.
"""

class OrchestratorError(Exception): pass
class ProviderError(OrchestratorError): pass
class RateLimitError(ProviderError): pass
class ConnectionFailure(ProviderError): pass

class ServiceProvider:
    def __init__(self, name: str, reliability: float):
        self.name = name
        self.reliability = reliability

    def call(self, data: str):
        import random
        if random.random() > self.reliability:
            raise ConnectionFailure(f"{self.name} is unreachable.")
        return f"Result from {self.name}"

class Orchestrator:
    def __init__(self, providers: list):
        self.providers = providers
        self.stats = {"attempts": 0, "failures": 0, "fallbacks": 0}

    def execute(self, payload: str):
        for provider in self.providers:
            self.stats["attempts"] += 1
            try:
                return provider.call(payload)
            except ProviderError as e:
                self.stats["failures"] += 1
                if provider != self.providers[-1]:
                    self.stats["fallbacks"] += 1
                print(f"Log: {e} -> Falling back.")
        return None

if __name__ == "__main__":
    providers = [
        ServiceProvider("Primary_Service", reliability=0.1),
        ServiceProvider("Backup_Service", reliability=1.0)
    ]
    orchestrator = Orchestrator(providers)
    
    response = orchestrator.execute("Data_Payload_01")
    print("-" * 20)
    print(f"Final Outcome: {response}")
    print(f"Observability Metrics: {orchestrator.stats}")
