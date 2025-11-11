"""
Generation service for combining retrieved documents into final text.
This is a simple concatenation approach without LLM integration.
"""
from typing import List
from app.models.domain import Document


def generate_section(user_text: str, documents: List[Document]) -> str:
    """
    Generate a section by combining retrieved documents.
    
    No LLM integration - this is a simple concatenation of document texts
    with a brief introduction providing context.
    
    Args:
        user_text: Original user query text
        documents: List of retrieved documents to combine
        
    Returns:
        Generated text combining the documents
    """
    if not documents:
        return "No relevant documents found for the requested section."
    
    # Create introduction
    intro = f"Based on {len(documents)} relevant document(s), here is the compiled content:\n\n"
    
    # Concatenate document texts with separators
    document_texts = []
    for i, doc in enumerate(documents, 1):
        separator = f"--- Document {i} (ID: {doc.id}) ---\n"
        document_texts.append(separator + doc.text)
    
    combined_text = intro + "\n\n".join(document_texts)
    
    return combined_text

