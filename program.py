from person import Admin, User, data
from json_scripts import read, write
from test import Test
import os
import hashlib

USERS_DATA = 'users.json'


def encode(string):
    return hashlib.md5(string.encode()).hexdigest()


def admin_registration():
    global data

    data['admin'][0] = (Admin(
        encode(input("Write username: ")),
        encode(input("Write  password: "))
    ).__dict__)

    write(data, USERS_DATA)


def user_registration():
    username = encode(input("Write username: "))
    while not is_unique(username):
        username = input("Write username: ")

    data['users'].append(User(
        username,
        encode(input("Write password: ")),
        input("Write full name: "),
        input("Write address: "),
        input("Write a phone number: ")
    ).__dict__)

    write(data, USERS_DATA)


# load user info from users.json
def loading():
    global data

    try:
        print("Hi!\n"
              "This is a testing program")
        data = read(USERS_DATA)

    except Exception:
        print("It is your first start and you need to register admin\n")
        admin_registration()


# Check that user login is unique
def is_unique(username):
    for i in range(len(data['users'])):
        if data['users'][i]['login'] == username:
            print("This username already exists")
            return False
    return True


# find login in base and return admin, user or none
def check_login_exists(username):
    if data['admin'][0]['login'] == username:
        return 'admin', data['admin'][0]
    else:
        for i in range(len(data['users'])):
            if data['users'][i]['login'] == username:
                return 'users', data['users'][i]

    return [None]


def user_menu(user):
    menu_item = -1
    while menu_item != '0':
        print(f'Hi {user["login"]}! Choose action\n'
              f'1 - Statistic\n'
              f'2 - Test\n'
              f'0 - Exit')
        menu_item = input()
        os.system('cls')
        if menu_item == '1':
            for key, value in user["test_statistic"].items():
                print(f'Test: "{key}" - grade: {value["grade"]}')
        elif menu_item == '2':
            show_tests(user)


def show_tests(user):
    new_test = Test("temp")
    new_test.load_tests()
    keys = list(new_test.test.keys())
    print("Choose test")
    for i in range(len(keys)):
        print(f'{i + 1} - {keys[i]}')

    num = int(input("Write a number of test"))
    os.system('cls')
    pass_test(new_test.test[keys[num - 1]], user, keys[num - 1])


def pass_test(test, user, test_name):
    grade = 0
    global data

    print(f"Want to start the test from begin?\n"
          f"1 - Yes\n"
          f"2 - Continue\n")
    if input() == '1':
        current_question = 0
    else:
        try:
            current_question = user["test_statistic"][test_name]["current_question"]
        except Exception:
            current_question = 0

    os.system('cls')

    for i in range(current_question, len(test)):
        print(test[i]['question_text'])
        print()
        for _ in test[i]['answers']:
            print(_)
        print("0 - Exit")
        answer = int(input("Write number of correct answer"))
        os.system('cls')
        if answer == 0:
            break
        elif answer - 1 == int(test[i]['correct_answer']):
            grade += 1

        user["test_statistic"].update({test_name: {"current_question": i, "grade": grade}})

    for i in range(len(data['users'])):
        if data['users'][i]['login'] == user["login"]:
            data['users'][i] = user

    write(data, USERS_DATA)


def admin_menu(admin):
    menu_item = -1
    while menu_item != '0':
        print(f'Hi {admin["login"]}! Choose action\n'
              f'1 - Change login and password\n'
              f'2 - Manage users\n'
              f'3 - Check statistic\n'
              f'4 - Manage tests\n'
              f'0 - Exit')
        menu_item = input()
        os.system('cls')
        if menu_item == '1':
            admin_registration()
            return
        elif menu_item == '2':
            manage_users()
        elif menu_item == '3':
            username = encode(input("Write username"))
            for i in range(len(data['users'])):
                if data['users'][i]['login'] == username:
                    get_statistic(data['users'][i])
        elif menu_item == '4':
            manage_tests()


def get_statistic(user):
    for key, value in user["test_statistic"].items():
        print(f'Test: "{key}" - grade: {value["grade"]}')


def manage_tests():
    test = Test("None")
    menu_item = -1
    while menu_item != '0':
        print(f'Choose action\n'
              f'1 - Add new test\n'
              f'2 - Delete test\n'
              f'0 - Exit')
        menu_item = input()
        os.system('cls')
        if menu_item == '1':
            test.test_name = input("Write a test name")
            test.create_test()
            test.save_test()
        elif menu_item == '2':
            test.delete_test(input("write a test name"))
        # elif menu_item == '3':
        #     test = load_test('tests.json', input("write a test name"))


def manage_users():
    menu_item = -1
    while menu_item != '0':
        print(f'Choose action\n'
              f'1 - Add new user\n'
              f'2 - Delete user\n'
              f'3 - Change user info\n'
              f'4 - Get user info\n'
              f'0 - Exit')
        menu_item = input()
        os.system('cls')
        if menu_item == '1':
            user_registration()
        elif menu_item == '2':
            delete_user(encode(input("Write username u want to delete")))
        elif menu_item == '3':
            change_user_info(encode(input("Write username u want to change")))
        elif menu_item == '4':
            get_user_info(encode(input("Write username u want to get")))


def change_user_info(username):
    for i in range(len(data['users'])):
        if data['users'][i]['login'] == username:
            get_user_info(username)
            tmp = input("What u want to change?")
            data['users'][i][tmp] = input("Change to ")
            write(data, USERS_DATA)


def get_user_info(username):
    for i in range(len(data['users'])):
        if data['users'][i]['login'] == username:
            print(data['users'][i])


def delete_user(username):
    for i in range(len(data['users'])):
        if data['users'][i]['login'] == username:
            del data['users'][i]
            write(data, USERS_DATA)
            print("Success!")
            return
    print("Something went wrong")


def log_in():
    login = check_login_exists(encode(input("Write your login")))
    password = encode(input("Write your password"))
    os.system('cls')
    if login[0] == 'admin':
        if login[1]['password'] == password:
            admin_menu(login[1])

    elif login[0] == 'users':
        if login[1]['password'] == password:
            user_menu(login[1])

    else:
        print("Wrong username or password!")


def start_program():
    loading()

    menu_item = -1
    while menu_item != '0':
        print(f'Choose action\n'
              f'1 - Log in\n'
              f'2 - Registration\n'
              f'0 - Exit')
        menu_item = input()
        os.system('cls')
        if menu_item == '1':
            log_in()
        elif menu_item == '2':
            user_registration()

    write(data, USERS_DATA)
