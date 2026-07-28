from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from backend.llm import load_llm

from backend.vector_store import VectorStore
from langchain.memory import ConversationBufferMemory


class RAGEngine:
    """
    Retrieves relevant document chunks and
    generates answers using LLM.
    """


    def __init__(self, api_key=None):

        self.vector_store = VectorStore()

        self.llm = load_llm()


        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="result"
        )



    def build_prompt(self):

        template = """

You are an intelligent study assistant.

Answer the question clearly using ONLY the provided documents.

If the answer is not available in the documents, say:
"I could not find that information in the provided documents."

Do not mention words like "context" or "provided context".

Document:
{context}

Question:
{question}

Answer:

"""


        return PromptTemplate(
            template=template,
            input_variables=[
                "context",
                "question"
            ]
        )



    def create_chain(self):

        prompt = self.build_prompt()


        retriever = (
            self.vector_store
            .load_vector_store()
            .as_retriever(
                search_kwargs={
                    "k":4
                }
            )
        )


        chain = RetrievalQA.from_chain_type(

            llm=self.llm,

            retriever=retriever,

            chain_type="stuff",

            memory=self.memory,

            chain_type_kwargs={
                "prompt":prompt
            },

            return_source_documents=True
        )


        return chain




    def ask(self, question):

        chain = self.create_chain()


        response = chain.invoke(
            {
                "query":question
            }
        )


        answer = response["result"]


        if response.get("source_documents"):

            doc = response["source_documents"][0]


            source = doc.metadata.get(
                "source",
                "Unknown"
            )


            page = doc.metadata.get(
                "page",
                0
            )


            answer += (
                f"\n\n📄 Source: {source}"
                f"\n📍 Page: {page+1}"
            )


        return answer




    def get_document_text(self):

        retriever = (
            self.vector_store
            .load_vector_store()
            .as_retriever(
                search_kwargs={
                    "k":20
                }
            )
        )


        docs = retriever.invoke(
            "Important concepts and topics from document"
        )


        document_text = "\n\n".join(
            doc.page_content
            for doc in docs
        )


        return document_text





    def generate_quiz(self):
        """
        Generate interactive quiz from study material.
        """


        document_text = self.get_document_text()



        prompt = f"""

You are an AI Study Assistant.

Create exactly 5 MCQ questions from the study material.

Return ONLY valid JSON.

Format:

[
 {{
 "question":"Question text",
 "options":[
 "Option A",
 "Option B",
 "Option C",
 "Option D"
 ],
 "answer":"Correct option exactly"
 }}
]


Rules:

- Exactly 5 questions.
- Four options each.
- Correct answer required.
- Use only study material.
- No markdown.
- No explanation.


Study Material:

{document_text}

"""


        response = self.llm.invoke(prompt)


        return response.content





    def generate_flashcards(self):

        document_text = self.get_document_text()


        prompt = f"""

You are an AI Study Assistant.

Create 10 flashcards from the study material.


Format:


Flashcard 1

Question:
...

Answer:
...


Rules:

- Keep questions short.
- Keep answers simple.
- Cover important concepts.
- Use only study material.


Study Material:

{document_text}

"""


        response = self.llm.invoke(prompt)


        return response.content





    def summarize_document(self):

        document_text = self.get_document_text()


        prompt = f"""

You are an AI Study Assistant.

Create a concise summary of this document.


Rules:

- Use bullet points.
- Maximum 8 points.
- Include important definitions.
- Mention key concepts.
- Simple language.


Study Material:

{document_text}

"""


        response = self.llm.invoke(prompt)


        return response.content