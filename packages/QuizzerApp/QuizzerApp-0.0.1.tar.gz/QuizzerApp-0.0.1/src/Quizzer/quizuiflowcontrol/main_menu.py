import os
import pkg_resources

from Quizzer.quizuiflowcontrol.quizmanager import QuizManager

class QuizApp:
    """
    A class to manage the Quiz Application user interface and flow.

    This class handles the interactions with the user, displays menu options, and
    facilitates the taking and managing of quizzes through the QuizManager.

    Attributes:
        user_name (str): Stores the user's name.
        quiz_manager (QuizManager): Manages the quizzes including listing and taking quizzes.
    """

    def __init__(self):
        """
        Initializes the QuizApp with an empty username and sets up the quiz manager.

        The quiz manager is initialized with the path to the quiz database, which is
        assumed to be in the 'db_quizzes' directory in the current working directory.
        """
        self.user_name = ""
        path_db_quizzes = pkg_resources.resource_filename('Quizzer', 'db_quizzes/')
        self.quiz_manager = QuizManager(path_db_quizzes)
        #self.quiz_manager = QuizManager(os.path.join(os.getcwd(), 'db_quizzes'))

    def run(self):
        """
        Starts the main loop of the application, handling the core workflow.

        This method is the entry point for the QuizApp. It displays the welcome message,
        prompts the user for their name, and then enters the main menu loop.
        """
        self.display_welcome_message()
        self.ask_user_name()
        self.main_menu()

    def display_welcome_message(self):
        """
        Displays a welcome message at the beginning of the application.
        """
        print("Welcome to the Quiz App")

    def ask_user_name(self):
        """
        Prompts the user to enter their name and stores it.

        The name entered by the user is stored in the user_name attribute.
        """
        self.user_name = input("What is your name? ")
        print(f"Welcome, {self.user_name}!\n")

    def main_menu(self):
        """
        Handles the main menu, allowing the user to choose different actions.

        The user can choose to list quizzes, take a quiz, or exit the app.
        The loop continues until the user chooses to exit.
        """
        while True:
            self.show_menu_options()
            user_choice = input("Your selection? ")

            if not user_choice:
                self.display_error_message()
                continue

            if user_choice.upper() == 'E':
                self.exit_app()
                break
            elif user_choice.upper() == 'L':
                self.list_quizzes()
            elif user_choice.upper() == 'T':
                self.take_quiz()
            else:
                self.display_error_message()

    def show_menu_options(self):
        """
        Displays the available menu options to the user.
        """
        print("Please make a selection")
        print("(L): List quizzes")
        print("(T): Take a quiz")
        print("(E): Exit the App")

    def display_error_message(self):
        """
        Displays an error message for invalid menu selections.

        This method is called when the user makes an invalid selection in the main menu.
        """
        print("Not a valid selection. Try again!")

    def exit_app(self):
        """
        Closes the application with a goodbye message.

        This method prints a goodbye message and then exits the main menu loop,
        effectively closing the application.
        """
        print("Exiting the Quiz App. Goodbye!")

    def list_quizzes(self):
        """
        Lists all the available quizzes using the QuizManager.

        This method calls the list_quizzes method of the quiz_manager to display
        all available quizzes to the user.
        """
        self.quiz_manager.list_quizzes()

    def take_quiz(self):
        """
        Facilitates the process of taking a quiz.

        The user is prompted to enter the number of the quiz they wish to take.
        The quiz is then administered by the QuizManager. If the quiz number is
        invalid, an error message is displayed.
        """
        try:
            quiz_number = int(input("Enter the quiz number: "))
            if quiz_number in self.quiz_manager.quizzes:
                print(f"You have selected quiz {quiz_number}")
                results = self.quiz_manager.take_quiz(quiz_number, self.user_name)
                print("Quiz completed. Here are your results:")
                self.quiz_manager.print_results()
                self.quiz_manager.save_results()
            else:
                print("Invalid quiz number.")
        except ValueError:
            self.display_error_message()

# Example usage:
# if __name__ == "__main__":
#    app = QuizApp()
#    app.run()


# Uncomment the below lines to run the Quiz App
if __name__ == "__main__":
     quiz_app = QuizApp()
     quiz_app.run()
