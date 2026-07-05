from models.llm import LLM


class RAG:

    def __init__(self):

        self.llm = LLM()

    def answer(self, retrieved_chunks, question):

        context = ""

        for chunk in retrieved_chunks:

            context += chunk["text"]

            context += "\n\n"

        answer = self.llm.generate(
            context,
            question
        )

        return answer