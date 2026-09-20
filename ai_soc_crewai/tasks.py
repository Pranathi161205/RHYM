from crewai import Task


def create_siem_task(siem_agent, incident):

    siem_task = Task(
        description=f"""
Analyze the SIEM data for incident {incident['incident_id']}.

Identify:

1. Suspicious events
2. Suspicious users
3. Suspicious IP addresses
4. Possible privilege escalation
5. Possible lateral movement
6. Relevant attack techniques

SIEM DATA:

{incident['siem_data']}
""",

        expected_output="""
Provide:

- Key SIEM findings
- Indicators of compromise
- Suspicious behavior
- Relevant MITRE ATT&CK techniques
- Confidence level
""",

        agent=siem_agent
    )

    return siem_task