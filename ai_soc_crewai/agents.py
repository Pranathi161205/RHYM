import os
from dotenv import load_dotenv
from crewai import Agent, LLM

load_dotenv()


class GroqLLM(LLM):

    def call(self, messages, **kwargs):

        # Remove CrewAI's cache_breakpoint
        if isinstance(messages, list):
            cleaned_messages = []

            for message in messages:
                if isinstance(message, dict):
                    message = message.copy()
                    message.pop("cache_breakpoint", None)

                cleaned_messages.append(message)

            messages = cleaned_messages

        return super().call(messages, **kwargs)


def create_siem_agent():

    llm = GroqLLM(
        model="groq/openai/gpt-oss-120b",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )

    siem_agent = Agent(
        role="SIEM Investigation Specialist",

        goal=(
            "Analyze SIEM security events and identify suspicious "
            "activities, attack patterns and potential indicators of compromise."
        ),

        backstory=(
            "You are an experienced SOC analyst specializing in SIEM "
            "investigation, log analysis, authentication anomalies, "
            "PowerShell activity and lateral movement."
        ),

        llm=llm,
        verbose=True
    )

    return siem_agent