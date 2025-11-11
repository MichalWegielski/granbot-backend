"""
Data Transfer Objects (DTOs) for API requests and responses.
These Pydantic models handle validation and serialization for the API layer.
"""
from typing import List
from pydantic import BaseModel, Field


class GenerateSectionRequest(BaseModel):
    """Request model for the generate-section endpoint."""
    company_id: str = Field(..., description="Company identifier")
    section_type: str = Field(..., description="Type of section to generate")
    text: str = Field(..., description="User query text")


class GenerateSectionResponse(BaseModel):
    """Response model for the generate-section endpoint."""
    company_id: str
    section_type: str
    generated_text: str
    sources: List[str] = Field(description="List of document IDs used in generation")
    request_id: str
    created_at: str


class HistoryResponse(BaseModel):
    """Response model for history entries."""
    request_id: str
    created_at: str
    company_id: str
    section_type: str
    sources: List[str]

