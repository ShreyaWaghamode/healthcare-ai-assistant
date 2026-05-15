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

            slots_text = "\n".join(
                tool_response["available_slots"]
            )

            tool_prompt = f"""
You are a healthcare appointment assistant.

You are answering ONLY based on the appointment slot data provided below.

DO NOT:
- mention documents
- mention missing information
- say "I could not find"
- talk about RAG or context
- hallucinate unavailable slots

User Question:
{question}

Department:
{tool_response['department']}

Available Slots:
{slots_text}

Instructions:
- Understand the user's request.
- If the requested day is unavailable, politely say it is unavailable.
- Suggest the nearest available slots.
- Keep the response short, natural, and professional.

Example Response:
"Sorry, there are no appointment slots available on Sunday. The nearest available slots are Monday at 10:00 AM, Monday at 02:00 PM, and Tuesday at 11:00 AM."

Answer:

"""

            final_answer = self.llm.generate(tool_prompt)

            return {
                "answer": final_answer
            }

        # RAG FLOW
        return rag_pipeline.ask(question)