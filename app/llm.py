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
#             model="gpt-4o-mini",

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

    def __init__(
        self,
        model="gemma3"
    ):

        self.model = model

    def generate(self, prompt):

        response = ollama.chat(

            model=self.model,

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]