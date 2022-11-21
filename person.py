class Person:
    login = ''
    password = ''

    def __init__(self, login, password):
        self.login = login
        self.password = password


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
            class_.exists = True
        return instances[class_]
    return getinstance


@singleton
class Admin(Person):
    exists = False

    def __init__(self, login, password):
        Person.__init__(self, login, password)


class User(Person):
    full_name = ''
    address = ''
    phone_number = ''

    def __init__(self, login, password, full_name, address, phone_number):
        Person.__init__(self, login, password)
        self.full_name = full_name
        self.address = address
        self.phone_number = phone_number
        self.test_statistic = {}


data = {
    "users": [],
    "admin": [{}]
}