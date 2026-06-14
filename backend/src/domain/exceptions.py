class TickerNotFoundError(Exception):
    """Raised when the requested ticker is not found in the external API."""
    pass

class RateLimitExceededError(Exception):
    """Raised when the external API rate limit is exceeded."""
    pass

class ConfigurationError(Exception):
    """Raised when application configuration is missing or invalid (e.g., API keys)."""
    pass

class ExternalServiceError(Exception):
    """Raised when an external service fails or is unreachable."""
    pass

class LLMParsingError(Exception):
    """Raised when an LLM fails to return the expected format (e.g., invalid JSON)."""
    pass

class InvalidDocumentFormatError(Exception):
    """Raised when an uploaded document has an invalid format or cannot be processed."""
    pass

class DataFetchError(Exception):
    """Raised when fundamental or historical data fails to be fetched from a provider."""
    pass

class DomainValidationError(Exception):
    """Raised when a domain entity violates business rules (e.g., negative prices)."""
    pass
