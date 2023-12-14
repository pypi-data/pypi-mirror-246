class NegativeAmountError(Exception):
    """User-defined exception for handling negative amount."""

    def __init__(self, message = "Input amount should be greater than or equal to zero."):
            
        self.message = message
        super().__init__(self.message)