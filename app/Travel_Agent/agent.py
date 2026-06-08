import chromadb
from sentence_transformers import SentenceTransformer
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# --- VECTOR DB INIT ---
client = chromadb.PersistentClient(path="C:/Analytics/Airline_Chatbot/travel_vectorstore")
collection = client.get_collection(name="travel_requirements")
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# --- TOOL: TRAVEL REQUIREMENT LOOKUP ---
def travel_requirement_lookup(query: str) -> dict:
    """
    Retrieve relevant travel policy snippets with their sources.
    Returns a structured dict usable by the LLM.
    """
    try:
        query_embedding = embed_model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=["documents", "metadatas"]
        )

        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]

        if not docs:
            return {"status": "NO_RESULTS", "data": []}

        data = []
        for doc, meta in zip(docs, metas):
            data.append({
                "content": doc.strip(),
                #"source": meta.get("source", "Travel Policy PDF")
            })

        return {"status": "OK", "data": data}

    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


# --- MODEL INIT ---
llm = LiteLlm(model="openai/gpt-4o-mini",temperature=0.5)


# --- AGENT SETUP ---
root_agent = Agent(
    name="Travel_Agent",
    model=llm,
    
    instruction="""
    You are a Visa & Travel Requirement Expert.
    * Ignore all non-travel messages silently — do not mention seats, meals, or other topics.
    * If non-travel messages are detected, then transfer to supervisor agent directly without any explanation.

    IMPORTANT RULES:
    1. For ANY travel-related question → ALWAYS call 'travel_requirement_lookup' BEFORE answering.

    2. This includes ALL follow-up questions:
    - passport validity
    - visa requirements
    - insurance
    - accommodation
    - travel documents

    3. MANDATORY RETRIEVAL:
    - ALWAYS search the knowledge base first.
    - DO NOT answer until retrieval is completed.

    4. STRICT ANSWERING (ANTI-HALLUCINATION):
    - Answer ONLY using retrieved document content.
    - DO NOT use your own knowledge.
    - DO NOT assume or infer missing details.
    - DO NOT generate information not present in retrieved data.

    5. INSUFFICIENT DATA HANDLING:
    - If retrieved data is missing, unclear, or incomplete:
        → Say: "I don't have enough information from the travel policy to answer this. Please refine your query."
    - DO NOT guess or fabricate answers.

    6. RESPONSE GROUNDING:
    - Every answer MUST be directly supported by retrieved content.
    - If a detail is not explicitly present → DO NOT include it.

    7. STRICT FAILURE RULES:
    - Answering without calling tool = FAILURE
    - Adding external knowledge = FAILURE
    - Guessing missing info = FAILURE

    ### TONE
    Professional, precise, and factual.
    """,
    tools=[travel_requirement_lookup]
)
