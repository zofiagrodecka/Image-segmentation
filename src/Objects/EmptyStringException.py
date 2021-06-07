class EmptyStringException(Exception):
    """Exception raised if a string is empty"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
