from app.tools import check_available_slots
from app.llm import OllamaLLM


class Agent:

    def __init__(self):

        self.llm = OllamaLLM()

    def decide_route(self, question):

        router_prompt = f"""
You are a healthcare AI routing agent.

Your task is to decide whether the user's question requires:

1. TOOL
Use TOOL ONLY when the user wants to PERFORM an action such as:
- booking an appointment
- checking doctor availability
- checking available slots
- scheduling a visit
- rescheduling appointments
- doctor timings

Examples:
- "Book an appointment with cardiology"
- "Show available slots"
- "What time is Dr. Smith available?"
- "Schedule my visit for tomorrow"

2. RAG
Use RAG when the user is:
- asking for information
- asking explanatory questions
- asking definitions or concepts
- asking healthcare FAQs
- asking policy questions
- asking educational questions

Examples:
- "What are scheduling methods?"
- "Explain appointment scheduling"
- "What is telehealth?"
- "How does insurance work?"
- "What are hospital policies?"

IMPORTANT:
- If the user is asking ABOUT something, choose RAG.
- If the user wants to DO something, choose TOOL.

Return ONLY one word:
TOOL
or
RAG

Question:
{question}

Answer:
"""

        decision = self.llm.generate(router_prompt)

        decision = decision.strip().upper()

        if decision not in ["TOOL", "RAG"]:
            decision = "RAG"

        return decision

    def route(self, question, rag_pipeline):

        decision = self.decide_route(question)

        print(f"\nROUTER DECISION: {decision}")

        # TOOL FLOW
        if decision == "TOOL":

            tool_response = check_available_slots()

            return {
                "answer":
                    f"Available slots for "
                    f"{tool_response['department']}:\n"
                    + "\n".join(
                        tool_response["available_slots"]
                    )
            }

        # RAG FLOW
        return rag_pipeline.ask(question)