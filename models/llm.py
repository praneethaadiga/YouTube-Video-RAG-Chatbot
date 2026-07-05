import ollama

from config import OLLAMA_MODEL


class LLM:

    def __init__(self):

        self.model = OLLAMA_MODEL

    def generate(self, context, question):

        prompt = f"""
You are a helpful AI assistant.

Answer ONLY from the given context.

If the answer is not present in the context, reply:

"I couldn't find that information in the video."

Context:

{context}

Question:

{question}

Answer:
"""

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