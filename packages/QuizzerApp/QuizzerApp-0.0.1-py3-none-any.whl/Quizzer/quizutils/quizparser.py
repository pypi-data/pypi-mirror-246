import json
from Quizzer.quizutils.quiz import Quiz, QuestionMC, QuestionTF, Answer

class JSONQuizParser:
    """
    The Quiz Parser object that is used for importing quiz data from JSON file.
    """

    def __init__(self):
        pass


    def import_data(self, quizpath):
        """
        Import data from json file.

        Parameters
        ----------
        quizpath : str
            the path of a JSON file that contains quiz data.

        Returns
        -------
        quiz_data : dictionary
            the dictionary that contains quiz data, such as questions, answers, choices.
        """
        with open(quizpath, 'r') as quizfile:
            quiz_data = json.load(quizfile)

        return quiz_data


    def create_question_obj(self, data):
        """
        Create question and answer objects and store the data in the object.
        All answer objects are stored in their question object.

        Parameters
        ----------
        data : dictionary
            the dictionray that stores quiz data.

        Returns
        -------
        question_obj : QuestionTF or QuestionMC object
            the question object that contains all question information,
            including question text, possible answers, correct answer, and point
        """

        # define question types
        if data['type'] == 'tf':
            question_obj = QuestionTF()

        elif data['type'] == 'mc':
            question_obj = QuestionMC()

            # add answer object to question object
            for a_data in data['choices']:
                answer = Answer()
                answer.name = a_data
                answer.text = data['choices'][a_data]
                question_obj.answers.append(answer)

        # define question text/correct answer/point
        question_obj.text = data['text']
        question_obj.correct_answer = data['answer']
        question_obj.points = int(data['points'])

        return question_obj


    def parse_quiz(self, quizpath):
        """
        Read the data in the JSON file and create the question objects, and
        stores them in the quiz object.

        Parameters
        ----------
        quizpath : str
            the path of a JSON file that contains quiz data.

        Returns
        -------
        new_quiz : Quiz object
            the quiz object that contains all question objects.
        """

        quiz_data = self.import_data(quizpath)

        new_quiz = Quiz()
        new_quiz.name = quiz_data['quizname']
        new_quiz.description = quiz_data['description']

        for q_data in quiz_data['questions']:

            question = self.create_question_obj(q_data)
            new_quiz.total_points += question.points
            new_quiz.questions.append(question)

        return new_quiz
