class Question:
    """
    This is the question object, needed for the result class
    """

    def __init__(self, **kwargs):
        self.maxQuestionScore = kwargs.get('ext_inspera_maxQuestionScore')
        self.questionId = kwargs.get('ext_inspera_questionId')
        self.questionTitle = kwargs.get('ext_inspera_questionTitle')
        self.autoScore = kwargs.get('ext_inspera_autoScore')
        self.durationSeconds = kwargs.get('ext_inspera_durationSeconds')
        self.candidateResponses = kwargs.get('ext_inspera_candidateResponses')
        self.questionContentItemId = kwargs.get('ext_inspera_questionContentItemId')
        self.questionNumber = kwargs.get('ext_inspera_questionNumber')
        self.questionWeight = kwargs.get('ext_inspera_questionWeight')
        self.manualScores = self.extract_manual_scores(kwargs.get('ext_inspera_manualScores', []))

    
    def extract_manual_scores(self, manual_scores):
        """
        Extracts manual scores from an exam, this will be the long answer questions.
        """
        if not manual_scores:
            return None
        return manual_scores[0].get('ext_inspera_manualScore')
