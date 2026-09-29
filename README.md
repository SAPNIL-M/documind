# DocuMind

DocuMind is a learning-focused RAG backend. It will let a user upload PDF or
plain text documents, ask questions about them, and receive answers grounded
in the uploaded content with source citations.

The project is being built slowly, one understandable step at a time. Read
`PROJECT_CONTEXT.md` before making project decisions or changing files.

## Current status

The project currently contains a minimal FastAPI application with a health
check. Document ingestion, embeddings, vector search, and answer generation
have not been implemented yet.

## Prerequisites

- Python 3.12
- PostgreSQL with the pgvector extension will be needed in a later phase
- An NVIDIA NIM API key will be needed when model integration is added

## Project structure

```text
documind/
├── PROJECT_CONTEXT.md
├── README.md
├── pyproject.toml
└── src/
    └── documind/
        ├── __init__.py
        ├── main.py
        └── api/
            ├── __init__.py
            └── health.py
```

## Running the API

Install the project and development dependencies with the Python package
manager used for the project. Then start the development server from the
project root:

```bash
uvicorn documind.main:app --reload
```

Because the application uses a `src` layout, configure the package path when
running directly from the project root if your environment does not install
the project first:

```bash
set PYTHONPATH=src
uvicorn documind.main:app --reload
```

On PowerShell, use:

```powershell
$env:PYTHONPATH = "src"
uvicorn documind.main:app --reload
```

Open the health endpoint at <http://127.0.0.1:8000/health>. It should return:

```json
{"status": "ok"}
```

FastAPI's interactive documentation is available at
<http://127.0.0.1:8000/docs>.

## Learning workflow

Before each implementation step, understand what the change solves, why it
belongs in the architecture, and how it will be verified. No file should be
changed without explicit approval. The next implementation phases will add
configuration, database access, document extraction, chunking, embeddings,
retrieval, and grounded answer generation.
