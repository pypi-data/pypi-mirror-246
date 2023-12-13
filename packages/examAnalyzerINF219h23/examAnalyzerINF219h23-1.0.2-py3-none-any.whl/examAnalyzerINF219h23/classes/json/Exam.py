from .ResultWrapper import ResultWrapper
import json


class Exam:
    """
    Represents an exam assessment generated from data sourced through the Inspera platform. This is the base class for every visualization

    Attributes:
        candidates (list): A list storing ResultWrapper instances representing individual candidates' results within the exam.
        lineItemSourcedId (str): Identifier for the exam's line item.
        assessmentRunTitle (str): Title of the assessment run.
        assessmentRunExternalId (str): External identifier for the assessment run.
        maxTotalScore (float): Maximum achievable total score for the exam.
        totalScore (float): Total score achieved in the exam.

    Methods:
        getCandidateScores(): Retrieves scores achieved by each candidate in the exam.
        getMaxScore(): Fetches the maximum achievable score within the exam.
        getQuestionIds(): Retrieves the question IDs in the correct order from the first candidate.
        getQuestionTitle(questionId): Retrieves the title of a specified question ID.
        getQuestionData(): Gathers data about each question, including its ID, number, and title.
        checkMultipleChoice(): Checks if questions are of the multiple-choice type.
        getQuestionNr(questionId): Retrieves the question number for a specified question ID.
        getCorrectPortion(questionId): Calculates the percentage of correct responses for a given question ID.

    Private Methods:
        _nrOfCandidates(): Retrieves the number of candidates who took the exam.
        _maxQuestionScore(questionId): Retrieves the maximum score achievable for a specific question ID.
    """

    def __init__(self, **kwargs):
        self.candidates = [ResultWrapper(**candidate_data).result
                           for candidate_data in kwargs.get('ext_inspera_candidates', [])]
        self.lineItemSourcedId = kwargs.get('lineItemSourcedId')
        self.assessmentRunTitle = kwargs.get('ext_inspera_assessmentRunTitle')
        self.assessmentRunExternalId = kwargs.get(
            'ext_inspera_assessmentRunExternalId')
        self.maxTotalScore = kwargs.get('ext_inspera_maxTotalScore')
        self.totalScore = kwargs.get('ext_inspera_totalScore')

    def getCandidateScores(self):
        """
        Gathers all the candidates scores
        """
        scores = [x.totalScore for x in self.candidates]
        return scores

    def getMaxScore(self):
        """
        Figures out the maximum score possible on the exam
        """
        max_score = self.candidates[0].maxScore
        return max_score

    def getQuestionIds(self):
        """
        Gets all questionIds from the first candidate in correct order
        """
        questionIds = []
        # Check if candidates list is not empty
        if self.candidates:
            first_candidate = self.candidates[0]  # Access the first candidate
            for question in first_candidate.questions:
                questionIds.append(question.questionId)
        return questionIds

    def getQuestionTitle(self, questionId):
        """
        Geths the question titles for each question
        """
        for candidate in self.candidates:
            for question in candidate.questions:
                if question.questionId == questionId:
                    return question.questionTitle
        return None

    def getQuestionData(self):
        """
        Gathers question id, question number and question title.
        """
        questionLabel = {}
        question_ids = self.getQuestionIds()
        for i in range(len(question_ids)):
            question_id = question_ids[i]
            question_title = self.getQuestionTitle(question_id)
            questionLabel[question_id] = f'Question {i + 1}: {question_title}'

        return questionLabel

    def checkMultipleChoice(self):
        """
        Checks if a question is a multiple choice question or
        long answer question.
        """
        multiple_choice = []
        # Check if candidates list is not empty
        if self.candidates:
            first_candidate = self.candidates[0]  # Access the first candidate
            for question in first_candidate.questions:
                if question.manualScores is None:
                    multiple_choice.append(True)
                else:
                    multiple_choice.append(False)
        return multiple_choice

    def getQuestionNr(self, questionId):
        """
        Correctly labels each question with their question number based on the question ids.
        """
        n = 1
        for qId in self.getQuestionIds():
            if qId == questionId:
                return 'Question ' + str(n)
            n += 1
        return "Unknown Question ID"

    def getCorrectPortion(self, questionId):
        """
        Returns the correct portion a student has on a question
        """
        total_scores = 0
        for candidate in self.candidates:
            for question in candidate.questions:
                if question.questionId == questionId:
                    # Check if manual score is available
                    if question.manualScores is not None:
                        total_scores += question.manualScores
                    else:
                        total_scores += question.autoScore

        count = self._nrOfCandidates()
        maxQuestionScore = self._maxQuestionScore(questionId=questionId)

        if count == 0:
            return None
        average_score = total_scores / count
        correct_portion = (average_score / maxQuestionScore) * 100
        return correct_portion

    # -- Private methods
    def _nrOfCandidates(self):
        return len(self.candidates)

    def _maxQuestionScore(self, questionId):
        for candidate in self.candidates:
            for question in candidate.questions:
                if question.questionId == questionId:
                    return question.maxQuestionScore
        return None
