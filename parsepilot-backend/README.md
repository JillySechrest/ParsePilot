# ParsePilot Backend

FastAPI backend for ParsePilot, a document-ingestion and question-answering service built around:

- Cognito JWT authentication
- S3-backed document storage
- Postgres metadata/vector search (planned)
- LLM-powered chat over uploaded documents (planned)

## Current Status

This repository is currently in scaffold/prototype state.

- API app bootstrap exists in `app/main.py`
- Route modules exist for documents and chat
- Several core service/data files are placeholders and still need implementation
- Dockerfile exists but is currently empty

Use this README as the source of truth for intended behavior while implementation is completed.

## Tech Stack

- Python 3.11+
- FastAPI + Uvicorn
- SQLAlchemy (planned integration in this repo)
- AWS: Cognito, S3, Bedrock (planned/in-progress)

## Project Layout

```text
parsepilot-backend/
├── app/
│   ├── auth/
│   │   └── cognito.py
│   ├── models/
│   │   └── database.py
│   ├── routes/
│   │   ├── chat.py
│   │   └── documents.py
│   ├── services/
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── llm.py
│   │   └── s3.py
│   ├── config.py
│   ├── db.py
│   └── main.py
├── requirements.txt
└── Dockerfile
```

## Quick Start (Local)

### 1. Create and activate a virtual environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the repository root.

Example:

```dotenv
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/parsepilot

# AWS
AWS_REGION=us-east-1
S3_BUCKET_NAME=parse-pilot-ingest

# Cognito
COGNITO_USER_POOL_ID=us-east-1_example
COGNITO_APP_CLIENT_ID=your_app_client_id
COGNITO_REGION=us-east-1

# Bedrock
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0
BEDROCK_EMBED_MODEL_ID=amazon.titan-embed-text-v2:0
```

Also ensure your AWS credentials are available (for example through environment variables or AWS CLI profile):

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` (if using temporary credentials)

### 4. Run the API

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open docs

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

Base URL (local): `http://localhost:8000`

### Health

- `GET /health` - API health check
- `GET /api/documents/health` - Documents route health
- `GET /api/chat/health` - Chat route health

### Documents

- `POST /api/documents/upload`
  - Auth required (Bearer JWT)
  - Form-data: `file`
  - Intended behavior:
    1. Validate extension and file size
    2. Upload source file to S3
    3. Create document record with `processing` status
    4. Trigger chunk/embed pipeline
    5. Return document id and status

### Chat

- `POST /api/chat/{document_id}/ask`
  - Auth required (Bearer JWT)
  - JSON body:
    ```json
    {
      "question": "What are the key terms in this contract?"
    }
    ```
  - Intended behavior:
    1. Verify ownership and readiness
    2. Embed question
    3. Vector search for relevant chunks
    4. Prompt LLM with context
    5. Save chat history
    6. Return answer

- `GET /api/chat/{document_id}/history`
  - Auth required (Bearer JWT)
  - Returns chronological chat messages for the document

## Authentication

Routes use Cognito JWT validation via a FastAPI dependency.

Client requests should send:

```http
Authorization: Bearer <access_token>
```

## Configuration Reference

The backend reads settings via `pydantic-settings` from `.env`.

| Variable | Required | Default | Purpose |
|---|---|---|---|
| `DATABASE_URL` | No | `postgresql://user:pass@localhost:3002/parsepilot` | Primary database connection |
| `AWS_REGION` | No | `us-east-1` | AWS region |
| `S3_BUCKET_NAME` | No | `parse-pilot-ingest` | Source document bucket |
| `COGNITO_USER_POOL_ID` | Yes | - | Cognito user pool |
| `COGNITO_APP_CLIENT_ID` | Yes | - | Cognito app client |
| `COGNITO_REGION` | No | `us-east-1` | Cognito region |
| `BEDROCK_MODEL_ID` | No | set in code | LLM model id |
| `BEDROCK_EMBED_MODEL_ID` | No | set in code | Embedding model id |

## Docker

A `Dockerfile` is present but currently empty. Container build/run support has not been wired yet.

## Known Gaps

The following areas are present in structure but still require implementation/fixes before production use:

- Database session and model definitions
- S3 upload service implementation
- Embeddings, vector search, and LLM service implementations
- Route import and typing cleanup in chat/auth modules
- Full integration tests

## Development Notes

- Keep route handlers thin; move business logic into `app/services`
- Prefer async-safe I/O for AWS and model calls
- Add tests for auth guards, upload validation, and chat flow

