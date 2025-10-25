# langchain_helper.py

# Standard library imports
import os
from typing import Sequence
from typing_extensions import Annotated, TypedDict

# Environment and API configuration
from dotenv import load_dotenv

# LangChain core components
from langchain_chroma import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain.chains.combine_documents import create_stuff_documents_chain

# Google Generative AI integration for LangChain
from langchain_google_genai import GoogleGenerativeAI

# LangGraph imports
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages

load_dotenv()


CHROMA_PATH = "chroma"

gpt4all_embeddings = GPT4AllEmbeddings(
    model_name="all-MiniLM-L6-v2.gguf2.f16.gguf",
    gpt4all_kwargs={'allow_download': 'True'}
)

db = Chroma(persist_directory=CHROMA_PATH,
            embedding_function=gpt4all_embeddings)

retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 7}
)

llm = GoogleGenerativeAI(
    model="gemini-2.5-flash-lite", 
    google_api_key=os.environ['GEMINI_API_KEY']
)

    
def contextualize_question():
    question_reformulation_prompt = """
    You are tasked with rewriting the latest user question into a fully standalone question.

    Guidelines:
    - Always include details from the chat history that clarify what the user means.
    - If the user follows up with vague phrases, 
    expand them into explicit standalone questions that combine the current wording 
    AND the relevant context from history.
    - Do NOT answer the question. Only rewrite it.
    - Do NOT return anything except valid JSON.
    """


    question_reformulation_template = ChatPromptTemplate.from_messages(
        [
            ("system", question_reformulation_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, question_reformulation_template 
    )
    
    return history_aware_retriever

def answer_question():
    answer_question_prompt = """ 
    Use the following pieces of retrieved context to answer the question. \
    You are a personal assistant specialized in topics about Orkun Sefik found in retrieved context. \
    Do NOT repeat the same answer, if you really have to, rephrase it. \
    Use one of the following formats: 
    - three to seven bullet points (not so long bullet points) followed by one or two sentences; 
    - just four to eight sentences (not so long sentences) maximum and keep the answer concise; in both cases, still give depth. Only if the user asks for more or less detail, adjust the depth of your answer. \
    IF the user asks for a reasoning, explain your thought process in a concise manner.\
    End your reply by asking if the user needs more help, but rephrase this question each time slightly. \
    Keep your tone natural, warm, and human. Your response should feel like it’s coming from a thoughtful assistant rather than a machine. \
    Do not use Emojis. \
    If the user’s question is unrelated to the retrieved context, politely refuse to answer and remind them of your scope. \
    ALWAYS reply in English, even if the user asks a question in another language. \
    
    {context}
    """ 

    
    answer_question_template = ChatPromptTemplate.from_messages(
        [
            ("system", answer_question_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    answer_question_chain = create_stuff_documents_chain(llm, answer_question_template)
    
    history_aware_retriever = contextualize_question()
    
    rag_chain = create_retrieval_chain(history_aware_retriever, answer_question_chain)
    
    return rag_chain


class State(TypedDict):
    """
    Represents the application state for a conversational workflow.

    Attributes
    ----------
    input : str
        The latest user query or input.
    chat_history : Annotated[Sequence[BaseMessage], add_messages]
        A sequence of messages representing the chat history, including user and AI messages.
    context : str
        The retrieved context relevant to the current query.
    answer : str
        The generated response to the user's query.
    """
    input: str
    chat_history: Annotated[Sequence[BaseMessage], add_messages]
    context: str
    answer: str


def build_history(chat_history, max_turns=2):
    """
    Shortens the chat history to the most recent turns, adding a summary if necessary.
    """
    if len(chat_history) <= max_turns * 2:
        return chat_history
    else:
        summary_message = AIMessage(
            content="Summary of earlier conversation:"
        )
        return [summary_message] + chat_history[-(max_turns*2):]



def call_model(state: State):
    """
    Retrieval-Augmented Generation zincirini çalıştırır ve hafızayı kısaltır.
    """
    rag_chain = answer_question()
    
    # Geçmişi kısalt
    short_history = build_history(state["chat_history"], max_turns=2)
    
    response = rag_chain.invoke({
        "input": state["input"],
        "chat_history": short_history
    })
    
    return {
        "chat_history": short_history + [
            HumanMessage(state["input"]),
            AIMessage(response["answer"]),
        ],
        "context": response["context"],
        "answer": response["answer"],
    }


workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

memory = MemorySaver()
app = workflow.compile(checkpointer=memory)


def execute_user_query(query_text):
    config = {"configurable": {"thread_id": "abc123"}}
    
    result = app.invoke(
        {"input": query_text},
        config=config,
    )
    
    return result["answer"]


if __name__ == "__main__":
    execute_user_query(query_text)

