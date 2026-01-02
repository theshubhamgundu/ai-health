import time
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.triage_agent import AroviaTriageAgent


def performance_test():
    """Measures the end-to-end latency of the triage process."""
    agent = AroviaTriageAgent()
    test_cases = [
        "I have a slight headache and a runny nose.",
        "I have had a high fever and a bad cough for three days.",
        "I am not able to eat pizza",
        "Can you book me a ticket",
        "I have severe chest pain and I am short of breath.",
    ]

    total_time = 0
    for i, text in enumerate(test_cases):
        start_time = time.time()
        _, _ = agent.analyze_symptoms_from_text(text)
        end_time = time.time()
        latency = end_time - start_time
        total_time += latency
        print(f"Test case {i+1}: Latency = {latency:.2f} seconds")

    average_latency = total_time / len(test_cases)
    print(f"\nAverage latency: {average_latency:.2f} seconds")

if __name__ == "__main__":
    performance_test()
