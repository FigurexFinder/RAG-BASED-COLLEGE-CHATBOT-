from fastapi import FastAPI, HTTPException
from langchain_groq import ChatGroq
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os
import re


load_dotenv()
app = FastAPI()

hugging_face_token = os.getenv("hugging_face_token")
embeddings = HuggingFaceEndpointEmbeddings(
            model="BAAI/bge-base-en-v1.5",
            huggingfacehub_api_token=hugging_face_token,
        )
new_db = FAISS.load_local("test-faiss-BAII-base", embeddings,allow_dangerous_deserialization=True)

prompt = ChatPromptTemplate.from_messages([
                    ("system", """You are a helpful assistant. Answer the user's question 
                    using ONLY the context provided below (Restructure the data accordingly). If the answer is not in the 
                    context, say 'I don't have enough information to answer this.'
     
                    Context:
                    {context}
                    """),
                    ("human", "{question}")
                ])
PLACEMENT_KEYWORDS = ["placement", "recruit", "package", "ctc", "lpa", "salary", "hired", "company", "companies", "placed"]
llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0,
    api_key=os.getenv("Groq_api_key")
)


def get_k(question: str) -> int:
    question_lower = question.lower()
    if any(keyword in question_lower for keyword in PLACEMENT_KEYWORDS):
        return 10   # wider retrieval for placement data spread across files
    return 5

def retrieve_context(query: str, score_threshold: float = 0.25):
    # Automatically pick k based on question topic
    k = get_k(query)

    results = new_db.similarity_search_with_relevance_scores(query, k=k)

    # Filter low-relevance results
    filtered = [(doc, score) for doc, score in results if score >= score_threshold]

    if not filtered:
        return "No relevant context found."

    # Combine all document contents into one context string
    context = "\n\n".join([
        f"[Source {i+1} | File: {doc.metadata.get('source_file', 'Unknown')} | Score: {score:.2f}]\n{doc.page_content}"
        for i, (doc, score) in enumerate(filtered)
    ])
    return context

def ask(question: str):
    context = retrieve_context(question)

    chain = prompt | llm
    response = chain.invoke({
        "context": context,
        "question": question
    })
    clean = re.sub(r"<think>.*?</think>", "", response.content, flags=re.DOTALL).strip()
    return clean

# Request body model
class ChatRequest(BaseModel):
    message: str

@app.get("/")
def index():
    return {"status": "OK"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        return {"response": ask(request.message)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))