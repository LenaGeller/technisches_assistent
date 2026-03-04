from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from pathlib import Path

CHROMA_DIR = Path(__file__).resolve().parent / "chroma_db"

COLLECTION_NAME = "fugen_und_dichtungen"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

db = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=str(CHROMA_DIR)
)

retriever = db.as_retriever(
    search_kwargs={"k": 12}
)
