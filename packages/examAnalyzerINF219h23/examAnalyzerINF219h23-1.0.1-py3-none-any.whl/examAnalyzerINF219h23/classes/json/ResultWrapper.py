from .Result import Result


class ResultWrapper:
    """
    This is the resultwrapper object, needed for the exam class
    """

    def __init__(self, result):
        self.result = Result(**result)
