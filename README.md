# Grantbot Backend

Backend API for grant application section generation. The application loads documents from a JSONL file, filters them by company and section type, ranks by text similarity, and combines them into generated sections.

## Features

- **Document Loading**: Loads documents from `./data/grantbot_vector_seed.jsonl` at startup
- **Section Generation**: Filters and ranks documents based on company_id, section_type, and text similarity
- **History Tracking**: Maintains in-memory history of all generation requests
- **Simple Retrieval**: Uses word overlap for document similarity (no external ML dependencies)
- **RESTful API**: FastAPI-based endpoints for generation and history

## Tech Stack

- Python 3.x
- FastAPI (HTTP framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- python-dotenv (environment configuration)

## Project Structure

```
granbot-backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app initialization
│   ├── models/
│   │   ├── __init__.py
│   │   ├── domain.py        # Internal domain models
│   │   └── dto.py           # API request/response models
│   ├── routes/
│   │   ├── __init__.py
│   │   └── sections_controller.py  # API endpoints
│   └── services/
│       ├── __init__.py
│       ├── data_service.py         # Document loading
│       ├── retrieval_service.py    # Document filtering/ranking
│       ├── generation_service.py   # Text generation
│       └── history_service.py      # History tracking
├── data/
│   └── grantbot_vector_seed.jsonl  # Source data
├── tests/
│   ├── __init__.py
│   └── test_sections.py     # API tests
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
└── README.md
```

## Installation

1. **Clone the repository** (if not already done)

2. **Create and activate virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

## Running the Application

Start the server with uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

**Interactive API documentation**:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### 1. Generate Section

**POST** `/generate-section`

Generate a section by finding and combining relevant documents.

**Request Body**:

```json
{
  "company_id": "123",
  "section_type": "innovation_description",
  "text": "AI automation SaaS RAG generator"
}
```

**Response**:

```json
{
  "company_id": "123",
  "section_type": "innovation_description",
  "generated_text": "Based on 3 relevant document(s), here is the compiled content:\n\n--- Document 1 (ID: doc-123-innovation-1) ---\nGrantbot.ai to aplikacja SaaS...",
  "sources": [
    "doc-123-innovation-1",
    "doc-123-innovation-en-1",
    "doc-123-market-1"
  ],
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "created_at": "2025-11-11T10:30:00.000000Z"
}
```

**cURL Example**:

```bash
curl -X POST "http://localhost:8000/generate-section" \
  -H "Content-Type: application/json" \
  -d '{
    "company_id": "123",
    "section_type": "innovation_description",
    "text": "AI automation SaaS RAG generator"
  }'
```

### 2. Get History

**GET** `/history/{company_id}`

Retrieve generation history for a specific company.

**Response**:

```json
[
  {
    "request_id": "550e8400-e29b-41d4-a716-446655440000",
    "created_at": "2025-11-11T10:30:00.000000Z",
    "company_id": "123",
    "section_type": "innovation_description",
    "sources": [
      "doc-123-innovation-1",
      "doc-123-innovation-en-1",
      "doc-123-market-1"
    ]
  }
]
```

**cURL Example**:

```bash
curl -X GET "http://localhost:8000/history/123"
```

### 3. Health Check

**GET** `/`

Simple health check endpoint.

**Response**:

```json
{
  "message": "Grantbot Backend API",
  "status": "running"
}
```

## Data Source

The application reads documents from `./data/grantbot_vector_seed.jsonl`. Each line in this file is a JSON object with the following structure:

```json
{
  "id": "doc-123-innovation-1",
  "company_id": "123",
  "section_type": "innovation_description",
  "language": "pl",
  "tags": ["AI", "SaaS"],
  "source_type": "knowledge_base",
  "source_url": null,
  "created_at": "2025-09-18T07:03:20.577543Z",
  "text": "Document content here..."
}
```

## How It Works

1. **Startup**: Documents are loaded from the JSONL file into memory
2. **Request**: Client sends company_id, section_type, and query text
3. **Filter**: Documents are filtered by company_id and section_type
4. **Rank**: Filtered documents are ranked by word overlap similarity with query text
5. **Select**: Top K documents (default: 3) are selected
6. **Generate**: Selected documents are combined into a single text
7. **Track**: Request metadata is saved to in-memory history
8. **Response**: Generated text and metadata are returned to client

## Configuration

Configuration is managed via environment variables. If a `.env` file is present in the root directory, it will be loaded at startup. You can use `.env.example` as a template.

| Variable    | Default                             | Description                     |
| ----------- | ----------------------------------- | ------------------------------- |
| `DATA_PATH` | `./data/grantbot_vector_seed.jsonl` | Path to JSONL data file         |
| `TOP_K`     | `3`                                 | Number of documents to retrieve |

## Testing

Run tests with pytest:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

Run with coverage:

```bash
pytest --cov=app
```

## Important Notes

- **No LLM Integration**: This version uses simple text concatenation, no external AI models
- **In-Memory Storage**: History is stored in memory and lost on restart
- **No Persistence**: No database - all data comes from the JSONL file
- **Simple Similarity**: Uses word overlap counting, not advanced embeddings
- **Document Fallback**: If no documents match company_id + section_type, falls back to company_id only

## Future Enhancements

Potential improvements for future versions:

- LLM integration for better text generation
- Database for persistent history
- TF-IDF or embedding-based similarity
- Caching layer for repeated queries
- Authentication/authorization
- Rate limiting
- Docker containerization

## License

[Specify your license here]
