class TickerNotFoundError(Exception):
    """Raised when the requested ticker is not found in the external API."""
    pass

class RateLimitExceededError(Exception):
    """Raised when the external API rate limit is exceeded."""
    pass
