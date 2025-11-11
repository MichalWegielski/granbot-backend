"""
Retrieval service for filtering and ranking documents.
Implements simple word-overlap similarity scoring without external dependencies.
"""
from typing import List
from app.models.domain import Document


def _calculate_word_overlap(text1: str, text2: str) -> int:
    """
    Calculate the number of common words between two texts.
    Uses simple tokenization (lowercase, split on whitespace).
    
    Args:
        text1: First text string
        text2: Second text string
        
    Returns:
        Number of common words between the two texts
    """
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    return len(words1.intersection(words2))


def retrieve_documents(
    documents: List[Document],
    company_id: str,
    section_type: str,
    query_text: str,
    top_k: int = 3
) -> List[Document]:
    """
    Filter and rank documents based on company_id, section_type, and query similarity.
    
    Strategy:
    1. Filter by company_id AND section_type
    2. If no matches, fallback to filtering by company_id only
    3. Rank filtered documents by word overlap similarity with query_text
    4. Return top_k documents
    
    Args:
        documents: List of all available documents
        company_id: Company identifier to filter by
        section_type: Section type to filter by
        query_text: User query text for similarity ranking
        top_k: Number of top documents to return
        
    Returns:
        List of top_k most relevant documents
    """
    # Step 1: Filter by company_id AND section_type
    filtered = [
        doc for doc in documents
        if doc.company_id == company_id and doc.section_type == section_type
    ]
    
    # Step 2: Fallback to company_id only if no exact matches
    # This ensures we always try to return something relevant
    if not filtered:
        filtered = [doc for doc in documents if doc.company_id == company_id]
        
        # If still no matches, use all documents as a last resort
        if not filtered:
            filtered = documents
    
    # Step 3: Rank by similarity to query text
    # Calculate word overlap score for each document
    scored_docs = []
    for doc in filtered:
        score = _calculate_word_overlap(query_text, doc.text)
        scored_docs.append((score, doc))
    
    # Sort by score descending (highest similarity first)
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    
    # Step 4: Return top_k documents
    top_docs = [doc for score, doc in scored_docs[:top_k]]
    
    return top_docs

