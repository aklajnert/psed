class Logger:
    """Logging utility"""

    verbosity = 0

    @classmethod
    def log(cls, message: str, level: int = 0):
        if cls.verbosity >= level:
            print(message)

    @classmethod
    def set_verbosity(cls, verbose: int):
        cls.verbosity = verbose
