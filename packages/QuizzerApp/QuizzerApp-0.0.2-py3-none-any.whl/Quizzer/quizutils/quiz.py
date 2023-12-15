import datetime
import sys
import time

class Quiz:
    """
    The Quiz object contains all information for quiz session, including
    questions, answers, and points.
            
    Attributes
    ----------
    name : str
        the quiz name
    description : str
        the quiz description
    questions : list
        the list of the question objects
    total_points : numeric
        the number of total score (only question's score)
    quiz_score : numeric
        the number of the quiz score (sum of the correct answer for question's score)
    correct_count : numeric
        the number of the correct answer
    quiz_score_ext : numeric
        the number of the quiz extra score (score based on time spending)
    quiz_score_final : numeric
        the number of the quiz score and extra score (sum of extra and question's score)
    time_start : datetime
        time when a user starts a quiz
    list_time_at_response : list
        the list of time usage for each question
    list_response : list
        the list of the user's answers
    list_qanswer : list
        the list of the correct answers (solution)
    list_qpoint : list
        the list of the question points
    list_score : list
        the list of the scores for each question (question's score)
    list_score_ext : list
        the list of the extra scores for each question
    list_score_final : list
        the lost of the summation scores (both extra and question's score)
    list_time_used : list
        the list of time usage for each question
    """

    def __init__(self):
        # quiz information from JSON file
        self.name = ""
        self.description = ""
        self.questions = []
        self.total_points = 0
        self.quiz_score = 0
        self.correct_count = 0

        # for logging score during the quiz session
        self.quiz_score_ext = 0
        self.quiz_score_final = 0
        self.time_start = None
        self.list_time_at_response = []
        self.list_response = []
        self.list_qanswer = []
        self.list_qpoint = []
        self.list_score = []
        self.list_score_ext = []
        self.list_score_final = []
        self.list_time_used = []


    def print_header(self, idx):
        """
        Print the main information of the quiz session.
        """
        print("\n\n", "*"*44)
        print(f"QUIZ NAME: {self.name}")
        print(f"DESCRIPTION: {self.description}")
        print(f"QUESTIONS: {idx+1}/{len(self.questions)}")
        print(f"TOTAL POINTS: {self.total_points}")
        print("*"*44, "\n")


    def print_results(self, quiztaker, thefile=sys.stdout):
        """
        Print the result information of the quiz session.
        """
        # overall results
        print("*"*44, "\n", file=thefile)
        print(f"RESULTS for {quiztaker}", file=thefile)
        print(f"Date: {datetime.datetime.today()}", file=thefile)
        print(f"QUESTIONS: {self.correct_count} out of {len(self.questions)} correct", file=thefile)
        print(f"SCORE: {self.quiz_score:.02f} points of possible {self.total_points:.02f}", file=thefile)
        print(f"SCORE EXTRA: {self.quiz_score_ext:.02f} points", file=thefile)
        print(f"TOTAL SCORE: {self.quiz_score_final:.02f} points", file=thefile)
        print("*"*44, "\n", file=thefile)

        # detail results
        print("\n", file=thefile)
        print("*"*14,"Result Details", "*"*14, "\n", file=thefile)

        ## detail for each question
        for idx, q in enumerate(self.questions):
            print(f"Question: {q.text}", file=thefile)
            print(f"Correct Answer: {q.correct_answer}", file=thefile)
            print(f"Your Answer: \t{q.log_response}", file=thefile)
            print(f"Time Spending: \t{self.list_time_used[idx]:.02f} seconds", file=thefile)
            print(f"Score: \t\t{self.list_score[idx]:.02f} points", file=thefile)
            print(f"Extra Score: \t{self.list_score_ext[idx]:.02f} points", file=thefile)
            print(f"Total Score: \t{self.list_score_final[idx]:.02f} points", file=thefile)
            print("-"*44, "\n", file=thefile)

        print(f"SCORE: \t{self.quiz_score:.02f} points of possible {self.total_points:.02f}", file=thefile)
        print(f"SCORE EXTRA: \t{self.quiz_score_ext:.02f} points", file=thefile)
        print(f"TOTAL SCORE: \t{self.quiz_score_final:.02f} points", file=thefile)
        print("*"*44, "\n", file=thefile)


    def take_quiz(self):
        """
        Run the quiz session. This provides the information of each question
        to the user and get the answer from them.

        Returns
        -------
        (self.quiz_score, self.correct_count, self.total_points) : tuple
            the tuple that contains the quiz score (question's score), 
            the number of correct answers, and the possible points.
        """
        self.score = 0
        self.correct_count = 0
        self.time_start = time.time()

        for idx, q in enumerate(self.questions):
            q.is_correct = False
            self.print_header(idx)
            q.ask()  # waiting for users' answer

            # count number of correct answers
            if q.is_correct:
                self.correct_count += 1

            print("------------------------------------------------\n")

        self.cal_score()

        return (self.quiz_score, self.correct_count, self.total_points)


    def cal_score(self):
        """
        Calculate score of the quiz session. This function calculates the question's score
        and extra score related to the user's time spending of each question.
        """

        # get data for calculating score
        ## get time, user's answers, question's points, and question's answer of each question
        for q_obj in self.questions:
            self.list_time_at_response.append(q_obj.log_time_at_res)  # user's time stamp
            self.list_response.append(q_obj.log_response)  # user's answer
            self.list_qanswer.append(q_obj.correct_answer)  # question's answer
            self.list_qpoint.append(q_obj.points)  # get question's point
        
        ## get time spending for each question in second unit
        for idx, _ in enumerate(self.list_time_at_response):
            if idx==0:
                time_used = self.list_time_at_response[idx] - self.time_start
            else:
                time_used = self.list_time_at_response[idx] - self.list_time_at_response[idx-1]
                
            self.list_time_used.append(time_used)

        # calculate score 
        ## comapre the corrected answers with answers from a user
        for idx, ans in enumerate(self.list_response):
            if ans==self.list_qanswer[idx]:
                self.list_score.append(float(self.list_qpoint[idx]))
            else:
                self.list_score.append(0.0)

        ## calculate extra score
        for itime_used in self.list_time_used:
            # get extra score if a user answers within 5 seconds. (maximum 5 points)
            # extra score reduce based on the ration (5/time spending).
            if itime_used<=5:
                if itime_used<1:
                    itime_used = 1  # if time used < 1, set as 1
                self.list_score_ext.append(5/itime_used)
            else:
                self.list_score_ext.append(0)

        ## combine question's scores and extra scores
        list_score_ext_correct = []
        for idx, q_score in enumerate(self.list_score):
            # user will get extra scores if their answer is correct.
            if q_score>0:
                score_cb = q_score + self.list_score_ext[idx]
                list_score_ext_correct.append(self.list_score_ext[idx])
                self.list_score_final.append(score_cb)
            else:
                self.list_score_ext[idx] = q_score
                self.list_score_final.append(q_score)

        ## calculate quiz score
        self.quiz_score = sum(self.list_score)
        self.quiz_score_ext = sum(list_score_ext_correct)
        self.quiz_score_final = sum(self.list_score_final)



class Question:
    """
    The Question object that stores all the question information for running the quiz session.
    """

    def __init__(self):
        self.points = 0
        self.correct_answer = ""
        self.text = ""
        self.is_correct = False
        self.log_response = None  # list of user's answers
        self.log_time_at_res = None  # list of time spending


class QuestionTF(Question):
    """
    The QuesionTF object (inherits from the Question object) 
    that stores the True or False question type. This object is used when 
    the program is waiting for the user's answer.
    """

    def __init__(self):
        super().__init__()

    # get the user's answer
    def ask(self):
        """
        Provide question information to the users and get reponse from them.
        """
        # print question text with T or F choices
        print(f"(T)rue or (F)alse: {self.text}")

        # get response
        while True:
            response = input("? ")

            # check response
            ## no response
            if len(response) == 0:
                print("Sorry, that's not a valid response.")
                print("Please try again.")
                continue

            ## reponse must be t or f (accept upper and lower cases)
            if response[0].lower() not in ["t", "f"]:
                print('Sorry, The valid response should be "t/T" or "f/F"')
                print("Please try again.")
                continue

            # convert response to the answer text (True/False)
            if response[0].lower()=='t':
                response_txt = "True"
            else:
                response_txt = "False"

            # check reponse
            self.is_correct = response_txt == self.correct_answer

            # log response
            self.log_response = response_txt
            self.log_time_at_res = time.time()

            break


class QuestionMC(Question):
    """
    The QuestionMC object (inherits from the Question object) 
    that stores the Multiple Choice question type. 
    This object is used when the program is waiting for the user's answer.  

    """

    def __init__(self):
        super().__init__()
        self.answers = []

    # get the user's answer
    def ask(self):
        # print question and choices
        print(self.text)
        for a in self.answers:
            print(f"{a.name}) {a.text}")
        
        # number of choices
        no_choices = len(self.answers)

        # get response
        while True:
            response = input("? ")

            # check response
            ## response should be number
            try:
                response_int = int(response)
            except:
                print(f"Sorry, that's not a valid response. The response should be a number between 1 to {no_choices}.")
                print("Please try again.")
                continue

            ## range answer number
            if (response_int > no_choices)|(response_int<1):
                print(f"Sorry, that's not a valid response. The response should be a number between 1 to {no_choices}.")
                print("Please try again.")
                continue 

            ## no reponse
            if not response:
                print("Sorry, that's not a valid response.")
                print("Please try again.")
                continue

            # get text of answer from answer number
            response_txt = self.answers[response_int-1].text
            self.is_correct = response_txt == self.correct_answer

            # log response
            self.log_response = response_txt
            self.log_time_at_res = time.time()
            break


class Answer:
    """
    The Answer object that stores the answers of each question. 
    """
    def __init__(self):
        self.text = ""
        self.name = ""
