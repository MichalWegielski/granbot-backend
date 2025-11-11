"""
Routes/endpoints for section generation and history.
"""
import uuid
from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
import os

from app.models.dto import (
    GenerateSectionRequest,
    GenerateSectionResponse,
    HistoryResponse
)
from app.models.domain import HistoryEntry
from app.services import data_service, retrieval_service, generation_service, history_service

router = APIRouter()


@router.post("/generate-section", response_model=GenerateSectionResponse)
def generate_section(request: GenerateSectionRequest) -> GenerateSectionResponse:
    """
    Generate a section based on company_id, section_type, and user text.
    
    Process:
    1. Retrieve all documents from data service
    2. Filter and rank documents by relevance
    3. Generate combined text from top documents
    4. Save request to history
    5. Return response with generated text and metadata
    """
    # Get all documents
    all_documents = data_service.get_all_documents()
    
    if not all_documents:
        raise HTTPException(
            status_code=503,
            detail="No documents available. Data file may not be loaded."
        )
    
    # Retrieve relevant documents
    top_k = int(os.getenv("TOP_K", "3"))
    top_documents = retrieval_service.retrieve_documents(
        documents=all_documents,
        company_id=request.company_id,
        section_type=request.section_type,
        query_text=request.text,
        top_k=top_k
    )
    
    # Generate section text
    generated_text = generation_service.generate_section(
        user_text=request.text,
        documents=top_documents
    )
    
    # Create metadata
    request_id = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat() + "Z"
    sources = [doc.id for doc in top_documents]
    
    # Save to history
    history_entry = HistoryEntry(
        request_id=request_id,
        created_at=created_at,
        company_id=request.company_id,
        section_type=request.section_type,
        sources=sources
    )
    history_service.add_entry(history_entry)
    
    # Return response
    return GenerateSectionResponse(
        company_id=request.company_id,
        section_type=request.section_type,
        generated_text=generated_text,
        sources=sources,
        request_id=request_id,
        created_at=created_at
    )


@router.get("/history/{company_id}", response_model=List[HistoryResponse])
def get_history(company_id: str) -> List[HistoryResponse]:
    """
    Get generation history for a specific company.
    
    Args:
        company_id: Company identifier
        
    Returns:
        List of history entries for the company
    """
    entries = history_service.get_by_company_id(company_id)
    
    return [
        HistoryResponse(
            request_id=entry.request_id,
            created_at=entry.created_at,
            company_id=entry.company_id,
            section_type=entry.section_type,
            sources=entry.sources
        )
        for entry in entries
    ]

