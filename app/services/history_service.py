"""
History service for tracking generation requests.
History is stored in-memory and not persisted across application restarts.
"""
from typing import List
from app.models.domain import HistoryEntry

# In-memory storage for history entries
_history: List[HistoryEntry] = []


def add_entry(entry: HistoryEntry) -> None:
    """
    Add a new history entry.
    
    Args:
        entry: HistoryEntry object to add to the history
    """
    _history.append(entry)


def get_by_company_id(company_id: str) -> List[HistoryEntry]:
    """
    Get all history entries for a specific company.
    
    Args:
        company_id: Company identifier to filter by
        
    Returns:
        List of HistoryEntry objects for the specified company
    """
    return [entry for entry in _history if entry.company_id == company_id]


def get_all() -> List[HistoryEntry]:
    """
    Get all history entries.
    
    Returns:
        List of all HistoryEntry objects
    """
    return _history

