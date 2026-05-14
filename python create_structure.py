import os

structure = {
    "app": {
        "main.py": "",
        "rag.py": "",
        "embeddings.py": "",
        "llm.py": "",
        "ingest.py": "",
        "vector_store.py": "",
        "agent.py": "",
        "config.py": ""
    },
    "data": {
        "document_1.txt": "",
        "document_2.txt": ""
    },
    "vector_store": {},
    "tests": {},
    "requirements.txt": "",
    "Dockerfile": "",
    "docker-compose.yml": "",
    "README.md": ""
}

def create_structure(base_path, tree):
    for name, content in tree.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # create empty file
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

if __name__ == "__main__":
    create_structure(".", structure)
    print("Exact project structure created successfully!")