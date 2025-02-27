class CalculationException(Exception):
    """
    Exception raised for calculation errors

        Attributes:
        message -- explanation of the error
    """

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
