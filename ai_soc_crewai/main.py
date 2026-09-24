import json
import csv

from agents import create_siem_agent
from tasks import create_siem_task


# Load incident data
with open("incident.json", "r", encoding="utf-8") as file:
    incident = json.load(file)


# Create SIEM Agent
siem_agent = create_siem_agent()


# Create SIEM Task
siem_task = create_siem_task(
    siem_agent,
    incident
)


# Execute the SIEM task
result = siem_agent.execute_task(siem_task)


# Convert result to text
result_text = str(result)


# Save agent output as CSV
with open("siem_output.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)

    writer.writerow(["Incident ID", "SIEM Agent Output"])
    writer.writerow([
        incident["incident_id"],
        result_text
    ])


# Display result
print("\n")
print("=" * 60)
print("SIEM AGENT INVESTIGATION RESULT")
print("=" * 60)

print(result)

print("\n")
print("=" * 60)
print("CSV FILE CREATED")
print("=" * 60)

print("File: siem_output.csv")