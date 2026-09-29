# DocuMind Project Context

This file is the handoff document for DocuMind. Read it before making decisions
about the project or changing the workspace. It is written so that another AI
agent can continue the work without relying on previous chat history.

## What DocuMind is

DocuMind is a learning-focused RAG-based backend AI project. A user will be
able to upload PDF or plain text documents, ask questions in plain English
about the document collection, and receive an answer grounded in those
documents with source citations.

RAG means Retrieval-Augmented Generation. Instead of asking an LLM to answer
from its general training alone, the application first retrieves relevant
sections from the project's documents and supplies those sections to the LLM as
context. The answer should therefore be based on the available source material,
and the system should avoid presenting unsupported guesses as facts.

The initial MVP is intentionally single-user and API-only. It will use Python,
FastAPI, PostgreSQL with pgvector, and hosted models accessed through the
NVIDIA NIM API using an API key. The model integration should be isolated
behind a small application boundary so that the provider or model can be
changed later without rewriting the RAG pipeline.

These are initial decisions for learning and portfolio purposes, not permanent
commitments. If implementation evidence suggests a change, explain the
tradeoff and ask for approval before changing the decision.

## Intended high-level workflow

The expected RAG pipeline is:

1. **Ingest** documents such as PDFs or text files.
2. **Parse and clean** the document contents.
3. **Chunk** the contents into useful passages.
4. **Embed** each passage into a vector representation.
5. **Store** passages and vectors in searchable storage.
6. **Retrieve** the passages most relevant to a user's question.
7. **Generate** an answer using the question and retrieved passages as context.
8. **Return grounding information**, such as source document and passage
   references, where appropriate.

This is the intended shape, not a requirement to implement everything at once.
The project should be built and understood incrementally. The first version
should make each stage visible rather than hiding the whole pipeline behind a
large framework abstraction.

## Initial architecture and data flow

### Document upload and ingestion

The first version uses synchronous processing so that the complete ingestion
pipeline is visible and easy to learn:

1. The client uploads a PDF or plain text file.
2. The API validates the file type and basic file properties.
3. The application creates a document record.
4. A parser extracts text and source metadata, including page information where
   the format supports it.
5. A chunker divides the extracted text into searchable passages.
6. The embedding provider creates a vector for each passage.
7. The application stores the document, chunks, metadata, and vectors in
   PostgreSQL with pgvector.
8. The API returns the completed document result or an explicit processing
   error.

Synchronous processing is appropriate for the first learning implementation
because it exposes the entire sequence in one request. It may be slow for
large documents. Background processing and job queues are intentionally
deferred until the core pipeline is understood.

### Question and answer flow

1. The client sends a question and may optionally provide a `document_id`.
2. The application embeds the question using the embedding provider.
3. pgvector retrieves the most relevant chunks. Without a document filter,
   retrieval searches the complete collection.
4. The application checks whether the retrieved context is sufficiently
   relevant.
5. If the context is insufficient, the API returns a clear qualification or
   refusal rather than inventing an answer.
6. Otherwise, the generation provider receives the question and retrieved
   context in a grounded prompt.
7. The API returns the generated answer and structured citations.

Each citation should contain the document ID, original filename, page number
when available, and chunk index. Citation metadata is returned as structured
data rather than relying only on text embedded in the generated answer.

### Initial API surface

The first API design includes:

| Capability | Purpose |
| --- | --- |
| Upload document | Validate and synchronously ingest a PDF or text file |
| List documents | Show the collection and processing metadata |
| Get document details | Inspect one document and its ingestion metadata |
| Delete document | Remove a document and its associated chunks |
| Ask question | Retrieve context and return a grounded answer with citations |

Exact route names, request schemas, and response schemas remain implementation
decisions and must be discussed before coding them.

### Service boundaries

Routes should coordinate application services and should not contain the RAG
implementation directly. The initial conceptual boundaries are:

- **Document service** — document lifecycle and metadata
- **Parser** — PDF/text extraction and source metadata
- **Chunker** — splitting extracted text into passages
- **Embedding provider** — converting text into vectors
- **Retrieval service** — vector similarity search and relevance filtering
- **Generation provider** — producing an answer from grounded context
- **Answer/orchestration service** — coordinating question processing and
  citation construction

The NVIDIA NIM provider-specific code should stay behind the embedding and
generation provider boundaries.

### Initial data entities

The first database design is centered on:

- **Document** — original filename, file type, ingestion status, timestamps,
  and any relevant extraction metadata
- **Chunk** — association to a document, chunk index, extracted text, page
  metadata where available, and embedding vector

The exact columns, relationships, indexes, status values, and migration
conventions remain open until the database-foundation phase.

### Important failure cases

The implementation must handle and expose errors for:

- Unsupported file type
- Empty, corrupt, or unreadable document
- Document with no extractable text
- Embedding or generation provider failure
- Database or vector search failure
- No sufficiently relevant context for a question
- Request for a missing document
- Deletion or partial ingestion failures

Errors should follow consistent API response conventions and must not be
silently converted into successful-looking results.

## Agreed MVP scope

### In scope

- Uploading and ingesting PDF and plain text files
- Extracting text and retaining useful source metadata, including document name
  and page information where available
- Chunking text into searchable passages
- Creating embeddings through the selected hosted model integration
- Storing documents, chunks, metadata, and vectors in PostgreSQL with pgvector
- Searching for relevant passages using vector similarity
- Generating answers using retrieved passages as context
- Returning citations or source references with answers
- Clearly qualifying or refusing answers when the retrieved context is
  insufficient
- A small, documented HTTP API with interactive FastAPI documentation
- Configuration through environment variables, especially the NVIDIA NIM API
  key and database connection details
- Unit and integration tests for the important ingestion, retrieval, and
  answer-grounding behavior

### Explicitly out of scope for the MVP

- A web frontend
- User registration, login, and multi-user authorization
- Multiple isolated users or tenants
- Background queues and distributed workers
- Advanced reranking, hybrid search, agentic workflows, or conversation memory
- Production deployment and infrastructure automation
- Fine-tuning models
- Supporting every document format

These features may be considered after the core pipeline works and is
understood.

## Initial technical direction

| Area | Initial decision |
| --- | --- |
| Language | Python |
| API framework | FastAPI |
| Relational database | PostgreSQL |
| Vector search | pgvector |
| Local database setup | Native PostgreSQL |
| Document formats | PDF and plain text |
| Model access | Hosted NVIDIA NIM API using an API key |
| Interface | Backend HTTP API only |
| User scope | Single user and one document collection |
| Grounding | Citations plus refusal/qualification when context is insufficient |
| Testing focus | Unit tests, API tests, database/retrieval tests, and basic RAG evaluation |

The NVIDIA NIM integration should use an OpenAI-compatible client or a thin
provider adapter where appropriate. Do not scatter provider-specific calls
through route handlers or retrieval code.

## Planned build phases

The implementation should proceed one focused step at a time. Each phase must
be explained and approved before files are changed.

1. **Scope and architecture** — confirm requirements, API boundaries, data
   flow, and terminology.
2. **Project foundation** — create the Python project structure, dependency
   configuration, environment configuration, and basic FastAPI application.
3. **Database foundation** — configure PostgreSQL connectivity, migrations,
   and the initial document/chunk data model.
4. **Document ingestion** — implement PDF/text validation, extraction,
   metadata handling, and persistence.
5. **Chunking and embeddings** — implement and test chunk boundaries and the
   embedding provider boundary.
6. **Vector retrieval** — store embeddings in pgvector and retrieve relevant
   chunks for a query.
7. **Answer generation** — construct grounded prompts, call the generation
   model, and return citations and insufficient-context behavior.
8. **API integration** — expose the smallest useful upload, ingestion/status,
   and question-answering endpoints with clear errors.
9. **Testing and evaluation** — create a small representative document set,
   test failure cases, and measure whether answers are grounded in retrieved
   context.
10. **Documentation and review** — document setup, architecture, tradeoffs,
    limitations, and possible next steps.

The order may change only after explaining why the change improves learning or
reduces unnecessary rework.

## Educational purpose

DocuMind is being built as a learning project and portfolio project. The goal
is to understand the architecture, tradeoffs, implementation details, failure
modes, and debugging process—not merely to obtain finished code.

An AI agent must not complete large portions of the project without teaching
what is being done. Prefer small, explainable steps. Before implementing a
piece, explain:

- what problem the piece solves;
- how it fits into the RAG system;
- the relevant design choices and alternatives;
- what the user should learn from the implementation; and
- how the change will be verified.

The user may ask to proceed one file at a time. Respect that pace. It is fine
to pause after each file or meaningful change and explain the result before
continuing.

For every proposed implementation step, explicitly identify the file(s) that
would change and wait for approval before modifying them.

## Mandatory change-approval rule

**Before making any file change, creating a file, installing dependencies,
running a formatter that writes files, or otherwise modifying the workspace,
ask the user explicitly for permission.**

Inspection-only actions are allowed without approval. This includes listing
files, reading files, searching code, and explaining possible approaches.

A prior broad request does not automatically approve later changes. Ask again
for each distinct implementation step or batch of changes, and clearly state
which files or workspace changes are proposed. Do not interpret silence as
approval.

When asking for approval, include:

- the exact file(s) to be changed or created;
- a concise explanation of the change;
- why the change is the next learning step; and
- the validation that will be performed afterward.

## Collaboration between AI agents

Different AI agents may work on DocuMind at different times because the user
may be using free tiers with usage limits. Every agent should:

- read this file before acting;
- preserve decisions already documented here and in the project files;
- avoid assuming that prior chat context exists;
- explain uncertainty instead of silently choosing;
- update project documentation when an approved decision changes the scope;
- make focused, reviewable changes; and
- leave the workspace in a clear state for the next agent.

If the project has not recorded a decision, treat it as undecided. Present
options and ask the user rather than inferring a permanent choice.

## Current status

- Project name: **DocuMind**
- Project type: Learning-focused RAG-based backend AI application
- Current phase: Scope agreed; implementation has not started
- Documents supported: PDF and plain text
- Backend framework: Python + FastAPI
- Database and vector store: PostgreSQL + pgvector
- Model access: NVIDIA NIM API via API key
- Interface: API-only
- User scope: Single user and one document collection
- Grounding behavior: Citations and refusal/qualification when context is insufficient
- Local database setup: Native PostgreSQL
- Authentication: Out of scope for the MVP
- Frontend: Out of scope for the MVP
- Deployment: Out of scope for the MVP

## Decisions still to make during implementation

The following details remain intentionally open and should be decided when
their implementation phase is reached:

- Exact Python version and dependency versions
- Exact NVIDIA NIM model names for generation and embeddings
- PDF extraction library and behavior for scanned/image-only PDFs
- Chunk size, overlap, and splitting strategy
- Embedding dimensionality and pgvector index configuration
- Exact database schema and migration conventions
- API route names and response schemas
- Retrieval threshold, top-k value, and insufficient-context policy
- Prompt format and citation representation
- Test document set and evaluation criteria

Do not silently turn these implementation details into permanent project
decisions. Explain the options and ask for approval when a choice affects the
architecture or user-visible behavior.

## Working agreement

Work slowly and collaboratively. The user is learning, so explanations and
review checkpoints are part of the deliverable. No implementation should begin
until the user has explicitly approved the proposed next change.
