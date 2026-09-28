import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM
from crewai_tools import NL2SQLTool

load_dotenv()

# --------------------------------------------------
# 1. PostgreSQL connection
# --------------------------------------------------

database_url = (
    f"postgresql://{quote_plus(os.getenv('POSTGRES_USER'))}:"
    f"{quote_plus(os.getenv('POSTGRES_PASSWORD'))}@"
    f"{os.getenv('POSTGRES_HOST')}:"
    f"{os.getenv('POSTGRES_PORT')}/"
    f"{os.getenv('POSTGRES_DB')}"
)

# --------------------------------------------------
# 2. CrewAI PostgreSQL Tool
# --------------------------------------------------

db_tool = NL2SQLTool(
    db_uri=database_url
)

# --------------------------------------------------
# 3. Groq LLM
# --------------------------------------------------

llm = LLM(
    model="groq/openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY")
)

# --------------------------------------------------
# 4. CrewAI Agent
# --------------------------------------------------

database_agent = Agent(
    role="Cybersecurity Database Analyst",

    goal=(
        "Analyze cybersecurity data stored in PostgreSQL "
        "and answer user questions by generating accurate "
        "SQL queries and interpreting the database results."
    ),

    backstory=(
        "You are a cybersecurity data analyst working with "
        "SIEM alerts, endpoint detection and response events, "
        "and threat intelligence data stored in PostgreSQL. "
        "Use the database tool whenever the user's question "
        "requires information from the database."
    ),

    tools=[db_tool],

    llm=llm,

    verbose=True
)

# --------------------------------------------------
# 5. Interactive Database Assistant
# --------------------------------------------------

print("\n==============================================")
print("   CYBERSECURITY DATABASE AI ASSISTANT")
print("==============================================")
print("Connected to PostgreSQL successfully.")
print("Available tables:")
print("  - threat_intel")
print("  - siem_alerts")
print("  - edr_events")
print("\nType 'exit' to quit.")
print("==============================================")

while True:

    user_question = input(
        "\nAsk a question about your cybersecurity database: "
    ).strip()

    if not user_question:
        continue

    if user_question.lower() == "exit":
        print("\nExiting Cybersecurity Database AI Assistant...")
        break

    # --------------------------------------------------
    # Create a task for the user's question
    # --------------------------------------------------

    task = Task(
        description=(
            f"Answer the following user question using the "
            f"PostgreSQL cybersecurity database:\n\n"
            f"{user_question}\n\n"
            f"Use the NL2SQLTool to query the database. "
            f"Do not invent database results. "
            f"Base the answer on the actual query results."
        ),

        expected_output=(
            "A clear and concise answer based on the "
            "actual PostgreSQL database results. "
            "Include relevant values, counts, or records "
            "when appropriate."
        ),

        agent=database_agent
    )

    # --------------------------------------------------
    # Create Crew
    # --------------------------------------------------

    crew = Crew(
        agents=[database_agent],
        tasks=[task],
        verbose=True
    )

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    try:

        result = crew.kickoff()

        print("\n====================================")
        print("FINAL ANSWER")
        print("====================================")
        print(result)
        print("====================================")

    except Exception as e:

        print("\n====================================")
        print("ERROR")
        print("====================================")
        print(e)
        print("====================================")