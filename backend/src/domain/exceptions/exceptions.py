class DomainValidationError(Exception):
    """Raised when a domain entity violates business rules (e.g., negative prices)."""
    pass
