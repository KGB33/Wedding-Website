class LFGIsFull(Exception):
    """
    Raised when a LFG excides capacity, or when an operation would cause an LFG to do so.
    """
