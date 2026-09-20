import json

from agents import create_siem_agent
from tasks import create_siem_task


# Load incident data
with open("incident.json", "r") as file:
    incident = json.load(file)


# Create SIEM Agent
siem_agent = create_siem_agent()


# Create SIEM Task
siem_task = create_siem_task(
    siem_agent,
    incident
)


# Execute the SIEM task
result = siem_agent.execute_task(
    siem_task
)


# Display result
print("\n")
print("=" * 60)
print("SIEM AGENT INVESTIGATION RESULT")
print("=" * 60)
print(result)