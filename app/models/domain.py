"""
Domain models for internal use in the application.
These models represent the data structure as it exists in the JSONL file
and internal application state.
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Document:
    """
    Represents a document loaded from the JSONL file.
    Matches the structure of records in grantbot_vector_seed.jsonl.
    """
    id: str
    company_id: str
    section_type: str
    language: str
    text: str
    tags: Optional[List[str]] = None
    source_type: Optional[str] = None
    source_url: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class HistoryEntry:
    """
    Represents a history entry for a generation request.
    Stored in-memory to track all generation requests.
    """
    request_id: str
    created_at: str
    company_id: str
    section_type: str
    sources: List[str]  # List of document IDs that were used

