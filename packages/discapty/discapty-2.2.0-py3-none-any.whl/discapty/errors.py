class NonexistingChallengeError(KeyError):
    """
    Raised when trying to get a challenge that does not exist.
    Subclass of "KeyError" as this error will appear when trying to get the challenge from a dict.
    """


class InvalidFontError(Exception):
    """
    Raised when one or more fonts are invalid.
    """


class ChallengeCompletionError(Exception):
    """
    Raised when a challenge has an issue regarding its completion.
    """


class TooManyRetriesError(ChallengeCompletionError):
    """
    Raised when a challenge received more retries than allowed.
    """


class AlreadyCompletedError(ChallengeCompletionError):
    """
    Raised when a challenge has already been completed.
    """


class AlreadyRunningError(ChallengeCompletionError):
    """
    Raised when a challenge is already running.
    """
