from pypdf import PdfReader
import chromadb
import ollama

# Local Chroma database
db = chromadb.PersistentClient(path="./rag_db")
collection = db.get_or_create_collection(name="study_documents")

EMBED_MODEL = "nomic-embed-text"


def create_embedding(text):
    response = ollama.embed(
        model=EMBED_MODEL,
        input=text
    )
    return response["embeddings"][0]


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def add_pdf_to_rag(pdf_file):
    text = extract_text_from_pdf(pdf_file)

    # Split text into chunks
    chunk_size = 1000
    chunks = [
        text[i:i + chunk_size]
        for i in range(0, len(text), chunk_size)
        if text[i:i + chunk_size].strip()
    ]

    embeddings = []

    for chunk in chunks:
        embeddings.append(create_embedding(chunk))

    ids = [f"chunk_{i}" for i in range(len(chunks))]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    return len(chunks)


def search_documents(query, n_results=3):
    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results["documents"][0] if results["documents"] else []