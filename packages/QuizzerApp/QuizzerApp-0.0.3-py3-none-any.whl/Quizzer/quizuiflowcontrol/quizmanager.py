import os
import datetime
import glob
import pkg_resources
from Quizzer.quizutils.quizparser import JSONQuizParser

class QuizManager:
    """
    A class responsible for managing the quizzes including listing, taking,
    and saving the results of quizzes.

    This class handles the loading and parsing of quiz files, user interactions
    for selecting and taking a quiz, and the storage of quiz results.

    Attributes:
        quizfolder (str): Path to the directory containing quiz files.
        the_quiz (Quiz): The currently selected quiz object.
        quizzes (dict): Dictionary mapping quiz IDs to quiz objects.
        results (Result): Results of the last taken quiz.
        quiztaker (str): Name of the user taking the quiz.
    """

    def __init__(self, quizfolder):
        """
        Initializes the QuizManager with a specific quiz folder path.

        Args:
            quizfolder (str): The path to the folder containing quiz files.

        Raises:
            FileNotFoundError: If the specified quiz folder does not exist.
        """
        self.quizfolder = quizfolder
        self.the_quiz = None
        self.quizzes = {}
        self.results = None
        self.quiztaker = ""

        if not os.path.exists(quizfolder):
            raise FileNotFoundError("The quiz folder doesn't exist!")

        self._build_quiz_list()

    def _build_quiz_list(self):
        """
        Builds a list of quizzes from JSON files located in the quiz folder.

        This private method scans the specified folder for JSON files and
        parses them to create Quiz objects, which are stored in the quizzes dictionary.
        """
        pattern = os.path.join(self.quizfolder, '*.json')
        json_files = glob.glob(pattern)

        for i, f in enumerate(json_files):
            parser = JSONQuizParser()
            self.quizzes[i + 1] = parser.parse_quiz(f)

    def list_quizzes(self):
        """
        Lists all available quizzes for the user.

        This method prints out each available quiz with its ID and name,
        as loaded from the quiz files.
        """
        for k, v in self.quizzes.items():
            print(f"({k}): {v.name}")

    def take_quiz(self, quizid, username):
        """
        Facilitates the process of taking a specified quiz by a user.

        Args:
            quizid (int): The ID of the quiz to be taken.
            username (str): The name of the user taking the quiz.

        Returns:
            Result: The results of the taken quiz.

        The method sets the current quiz based on the provided ID, records the user's name,
        and invokes the quiz taking process. It then returns the results of the quiz.
        """
        self.quiztaker = username
        self.the_quiz = self.quizzes[quizid]
        self.results = self.the_quiz.take_quiz()
        return self.results

    def print_results(self):
        """
        Prints the results of the last taken quiz.

        This method calls the print_results method of the current quiz object,
        displaying the results to the user.
        """
        self.the_quiz.print_results(self.quiztaker)

    def save_results(self):
        """
        Saves the results of the quiz in a uniquely named file.

        The results are saved in a text file with a name based on the current date
        and a sequence number to ensure uniqueness. The file is saved in the 'db_results'
        directory within the current working directory.
        """
        today = datetime.datetime.now()
        filename = f"QuizResults_{today.year}_{today.month}_{today.day}.txt"
        n = 1
        while os.path.exists(filename):
            filename = f"QuizResults_{today.year}_{today.month}_{today.day}_{n}.txt"
            n += 1

        #path_cur = os.getcwd()
        #path_result = os.path.join(path_cur, 'db_results', filename)
        path_cur = pkg_resources.resource_filename('Quizzer', 'db_results/')
        path_result = os.path.join(path_cur,filename)
        with open(path_result, "w") as f:
            self.the_quiz.print_results(self.quiztaker, f)

# Example usage:
if __name__ == "__main__":
    quiz_manager = QuizManager('path/to/quizfolder')
    quiz_manager.list_quizzes()
    selected_quiz_id = 1  # assuming the user selects quiz 1
    quiz_manager.take_quiz(selected_quiz_id, 'Alice')
    quiz_manager.print_results()
    quiz_manager.save_results()
