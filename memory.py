import chromadb

# Create local memory database
client = chromadb.PersistentClient(path="./memory_db")

# Create a collection for student memory
collection = client.get_or_create_collection(
    name="student_memory"
)

def save_memory(question, answer):
    collection.add(
        documents=[f"Question: {question}\nAnswer: {answer}"],
        ids=[f"memory_{collection.count() + 1}"]
    )

def get_memories(question):
    results = collection.query(
        query_texts=[question],
        n_results=3
    )

    return results["documents"][0] if results["documents"] else []