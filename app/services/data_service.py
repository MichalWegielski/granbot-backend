"""
Data service for loading and managing documents from the JSONL file.
Documents are loaded at application startup and stored in memory.
"""
import json
import os
from typing import List
from app.models.domain import Document

# In-memory storage for documents
_documents: List[Document] = []


def load_documents() -> None:
    """
    Load documents from the JSONL file specified in config.
    Each line in the file is a JSON object representing a document.
    Documents are stored in the module-level _documents list.
    """
    global _documents
    _documents = []
    
    data_path = os.getenv("DATA_PATH", "./data/grantbot_vector_seed.jsonl")

    try:
        with open(data_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                data = json.loads(line)
                doc = Document(
                    id=data.get("id"),
                    company_id=data.get("company_id"),
                    section_type=data.get("section_type"),
                    language=data.get("language"),
                    text=data.get("text"),
                    tags=data.get("tags"),
                    source_type=data.get("source_type"),
                    source_url=data.get("source_url"),
                    created_at=data.get("created_at")
                )
                _documents.append(doc)
        
        print(f"Loaded {len(_documents)} documents from {data_path}")
    except FileNotFoundError:
        print(f"Warning: Data file not found at {data_path}")
        _documents = []
    except Exception as e:
        print(f"Error loading documents: {e}")
        _documents = []


def get_all_documents() -> List[Document]:
    """
    Get all loaded documents.
    
    Returns:
        List of Document objects loaded from the JSONL file.
    """
    return _documents

