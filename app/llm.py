# from openai import OpenAI
# from app.config import OPENAI_API_KEY
import ollama


# class LLM:

#     def __init__(self):

#         self.client = OpenAI(
#             api_key=OPENAI_API_KEY
#         )

#     def generate(self, prompt):

#         response = self.client.chat.completions.create(
#       
# 
# 
# 
#       model="gpt-4o-mini",

#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],

#             temperature=0.1
#         )

#         return response.choices[0].message.content





class OllamaLLM:

    def __init__(self, model="gemma3"):
        self.model = model

    def generate(self, prompt):

        system_prompt = """
You are a strict healthcare AI assistant.

Rules:
- Answer ONLY using the provided context.
- If the answer is not in the context, say: "I could not find this information in the provided documents."
- Do NOT guess or hallucinate.
- Do NOT provide medical diagnosis.
- Keep answers short, clear, and professional.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]