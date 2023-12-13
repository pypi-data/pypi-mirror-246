from .Question import Question


class Result:
    """
    This is the result object, needed for the result wrapper class
    """
    def __init__(self, **kwargs):
        self.questions = [Question(**question_data)
                          for question_data in kwargs.get('ext_inspera_questions', [])]
        self.autoScore = kwargs.get('ext_inspera_autoScore')
        self.maxScore = self.calculate_max_score()
        self.candidateId = kwargs.get('ext_inspera_candidateId')
        self.sourcedId = kwargs.get('sourcedId')
        self.userAssessmentSetupId = kwargs.get(
            'ext_inspera_userAssessmentSetupId')
        self.userAssessmentId = kwargs.get('ext_inspera_userAssessmentId')
        self.dateLastModified = kwargs.get('dateLastModified')
        self.startTime = kwargs.get('ext_inspera_startTime')
        self.endTime = kwargs.get('ext_inspera_endTime')
        self.extraTimeMins = kwargs.get('ext_inspera_extraTimeMins')
        self.incidentTimeMins = kwargs.get('ext_inspera_incidentTimeMins')
        self.attendance = kwargs.get('ext_inspera_attendance')
        self.lineItem = kwargs.get('lineItem')
        self.student = kwargs.get('student')
        self.finalGradeDate = kwargs.get('ext_inspera_finalGradeDate')
        self.finalGrade = kwargs.get('ext_inspera_finalGrade')
        self.totalScore = kwargs.get('ext_inspera_totalScore')
        self.score = kwargs.get('score')

    def calculate_max_score(self):
        return sum(question.maxQuestionScore for question in self.questions)
