from json_scripts import read, write

TESTS_FILE = 'tests.json'


class Test:
    def __init__(self, test_name):
        self.current_test = 0
        self.tested_user = ''
        self.test = {}
        self.test_name = test_name

    def create_test(self):
        self.test = {self.test_name: []}
        for i in range(3):
            self.test[self.test_name].append(Question(
                input("Write question"),
                [input("Write a first answer"), input("Write a second answer"), input("Write a third answer")],
                input("Write a number of correct answer (0 - 2)")
            ).__dict__)
        self.save_test()

    def save_test(self):
        try:
            tmp = read(TESTS_FILE)
            tmp.update(self.test)
            write(tmp, TESTS_FILE)
        except Exception:
            print("Something went wrong")
        write(self.test, TESTS_FILE)

    def delete_test(self, name):
        try:
            test = read(TESTS_FILE)
            _ = test.pop(name)
            write(test, TESTS_FILE)
        except KeyError:
            print("Cant find this test!")

    def load_tests(self):
        try:
            self.test = read(TESTS_FILE)

        except Exception:
            print("Something goes wrong\n"
                  "Try to another file or test name")


class Question:

    def __init__(self, question_text, answers, correct_answer):
        self.question_text = question_text
        self.answers = answers
        self.correct_answer = correct_answer


