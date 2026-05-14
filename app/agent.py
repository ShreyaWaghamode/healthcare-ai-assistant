from openai import OpenAI
from app.tools import check_available_slots
from app.llm import OllamaLLM


class Agent:

    def __init__(self):

        self.llm = OllamaLLM()
        #self.llm = OpenAI

    def decide_route(
        self,
        question
    ):

        router_prompt = f"""
You are an intelligent routing agent.

Your task is to decide whether the user question needs:

1. TOOL
- Use TOOL only if user wants:
    - booking appointment
    - scheduling
    - checking available slots
    - doctor timings

2. RAG
- Use RAG for:
    - hospital policies
    - insurance
    - telehealth
    - appointment confirmation
    - cancellation policy
    - medication
    - FAQs
    - document-based questions

Return ONLY one word:
TOOL
or
RAG

QUESTION:
{question}

ANSWER:
"""

        decision = self.llm.generate(
            router_prompt
        )

        return decision.strip().upper()

    def route(
        self,
        question,
        rag_pipeline
    ):

        decision = self.decide_route(
            question
        )

        print(f"\nROUTER DECISION: {decision}")

        # TOOL FLOW
        

        if "TOOL" in decision:

            tool_response = (
                check_available_slots()
            )

            return {
                "answer": (
                    f"Available slots for "
                    f"{tool_response['department']}:\n"
                    + "\n".join(
                        tool_response[
                            "available_slots"
                        ]
                    )
                ),

                "sources": [],

                "confidence": "high"
            }

        # RAG FLOW

        return rag_pipeline.ask(question)