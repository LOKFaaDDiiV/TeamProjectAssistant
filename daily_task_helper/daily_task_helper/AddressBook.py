import re
import sys
import os
import pickle
from pathlib import Path
from collections import UserDict
from datetime import *


# ---------- Class part ----------

class NameArgumentError(Exception):
    pass


class PhoneArgumentError(Exception):
    pass


class PhoneExistsError(Exception):
    pass


class PhoneDoesNotExistError(Exception):
    pass


class NoNameError(Exception):
    pass


class BirthFormatError(Exception):
    pass


class SearchValueError(Exception):
    pass


class NameExistsError(Exception):
    pass


class EmailExistsError(Exception):
    pass


class EmailDoesNotExistError(Exception):
    pass


class CustomIterator:
    def __init__(self, value, n):
        self.dicts = value
        self.n = n
        self.key = []
        for i in value:
            self.key.append(i)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.key):
            self.iter_dicts = {}
            for i in range(self.n):
                if len(self.key):
                    self.iter_dicts.update([(self.key[0], self.dicts.pop(self.key[0]))])
                    del self.key[0]
                else:
                    break

            return self.iter_dicts
        raise StopIteration


class AddressBook(UserDict):
    def iterator(self, n=10, some_dict=None):
        if not bool(self.data):
            return "Address book is empty!"
        if some_dict is None:
            return CustomIterator(self.data.copy(), n)
        else:
            return CustomIterator(some_dict.copy(), n)

    def add_record(self, record):
        self.data[record.name.value] = record

    def search(self, name=None, phone=None, email=None):
        result_list = []
        if name:
            for k, v in self.data.items():
                if re.search(name, k, flags=re.IGNORECASE):
                    result_list.append(v)
        elif phone:
            for v in self.data.values():
                for i in v.phones:
                    if re.search(phone, i.value):
                        result_list.append(v)
                        break
        elif email:
            for v in self.data.values():
                for i in v.emails:
                    if re.search(email, i.value):
                        result_list.append(v)
                        break
        return result_list

    def delete_record(self, name):
        del self.data[name]


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    @property
    def var(self):
        return self.value

    @var.setter
    def var(self, new_value):
        self.value = new_value


class Phone(Field):
    @property
    def var(self):
        return self.value

    @var.setter
    def var(self, new_value):
        if re.fullmatch(r"\+?[0-9]+", new_value):
            self.value = new_value
        else:
            print("Wrong phone format, try again. A phone number can only contain numbers and a '+' at the beginning")


class Birthday(Field):
    @property
    def var(self):
        return self.value

    @var.setter
    def var(self, new_value):
        if re.fullmatch(r"[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}", new_value):
            self.value = new_value
        else:
            print("Wrong date format, try again. Please use dd.mm.yyyy format")


class Email(Field):
    @property
    def var(self):
        return self.value

    @var.setter
    def var(self, new_value):
        if re.fullmatch(r"[\w.%-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}", new_value):
            self.value = new_value
        else:
            print("Wrong email format, try again")


class Record:
    def __init__(self, name, phone=None, birthday=None, email=None):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        if phone:
            self.phones.append(Phone(phone))
        self.birthday = Birthday(birthday)
        if email:
            self.emails.append(Email(email))

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday.var = birthday

    def add_mail(self, email):
        self.emails.append(Email(email))

    def change_phone(self, old, phone):
        for i in self.phones:
            if i.value == old:
                pos = self.phones.index(i)
                self.phones[pos].var = phone

    def change_mail(self, old, email):
        for i in self.emails:
            if i.value == old:
                pos = self.emails.index(i)
                self.emails[pos].var = email

    def delete_phone(self, phone):
        for i in self.phones:
            if i.value == phone:
                self.phones.remove(i)

    def delete_email(self, email):
        for i in self.emails:
            if i.value == email:
                self.emails.remove(i)

    def days_to_birthday(self, flag=False):
        if self.birthday.value:
            current_date = datetime.now().date()
            birth_date = datetime.strptime(self.birthday.value, "%d.%m.%Y").date()
            if birth_date.month >= current_date.month and birth_date.day >= current_date.day:
                if birth_date.day != current_date.day:
                    birth_date = birth_date.replace(year=current_date.year)
                    res = birth_date - current_date
                    if flag:
                        return f"Days left until the birthday: {res.days}"
                    else:
                        return res.days
                else:
                    if flag:
                        return f"This day is today!"
                    else:
                        return 0
            else:
                birth_date = birth_date.replace(year=current_date.year + 1)
                res = birth_date - current_date
                if flag:
                    return f"Days left until the birthday: {res.days}"
                else:
                    return res.days
        else:
            return None


# ---------- End of class part ----------
# ---------- Func part ----------


def input_error(func):
    def inner(*a, **k):
        try:
            return func(*a, **k)
        except TypeError:
            return "TypeError???What???"
        except AttributeError:
            return "Якщо це повідомлення вилізло, то розробник десь накосячив :)"
        except IndexError:
            return "You entered wrong index, try again"
        except ValueError:
            return "You entered a wrong nuber of arguments, try again"
        except KeyError:
            return "Unknown command. Type 'help' to show a list of commands"
        except NameArgumentError:
            return "Wrong name format, try again. The name can contain only letters of the Latin alphabet"
        except NameExistsError:
            return "This contact already exist in address book"
        except PhoneArgumentError:
            return "Wrong phone format, try again. A phone number can only contain numbers and a '+' at the beginning"
        except PhoneExistsError:
            return "This phone number already exist in address book"
        except PhoneDoesNotExistError:
            return "Phone number does not exist"
        except NoNameError:
            return "Contact with that name does not exist"
        except BirthFormatError:
            return "Wrong birthday date format"
        except SearchValueError:
            return "You entered wrong search request"
        except EmailExistsError:
            return "This email already exist in address book"
        except EmailDoesNotExistError:
            return "Email does not exist"

    return inner


# --- add part ---


@input_error
def add_user(data, *args, **kwargs):
    name = data.get("name")
    key = name.capitalize()
    if key not in address_book.keys():
        address_book.add_record(Record(key))
        return f"Contact {key} successfully created"
    else:
        raise NameExistsError


@input_error
def add_phone(data, *args, **kwargs):
    name = data.get("name")
    phone_number = data.get("phone")
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    if number_checker(phone_number):
        raise PhoneExistsError
    address_book[key].add_phone(phone=phone_number)
    return f"Phone number {phone_number} successfully added to {key}'s contact"


@input_error
def add_email(data, *args, **kwargs):
    name = data.get("name")
    email = data.get("email")
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    if mail_checker(email):
        raise EmailExistsError
    address_book[key].add_mail(email=email)
    return f"Email for {key}'s contact set to {email}"


@input_error
def add_birthday(data, *args, **kwargs):
    name = data.get("name")
    birth = data.get("birthday")
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    address_book[key].add_birthday(birthday=birth)
    return f"{birth} set as birthday for {key} contact"
    pass


# --- change part ---


@input_error
def change_phone(data, *args, **kwargs):
    name = data.get("name")
    old_phone_number = data.get("old phone")
    new_phone_number = data.get("new phone")
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    if number_checker(new_phone_number):
        raise PhoneExistsError
    if not number_checker(old_phone_number):
        raise PhoneDoesNotExistError
    address_book[key].change_phone(old=old_phone_number, phone=new_phone_number)
    return f"{key}'s {old_phone_number} phone number successfully changed on {new_phone_number}"


@input_error
def change_email(data, *args, **kwargs):
    name = data.get("name")
    old_email = data.get("old email")
    new_email = data.get("new email")
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    if mail_checker(new_email):
        raise EmailExistsError
    if not mail_checker(old_email):
        raise EmailDoesNotExistError
    address_book[key].change_mail(old=old_email, email=new_email)
    return f"{key}'s {old_email} email successfully changed on {new_email}"


# --- delete part ---


@input_error
def delete_user(data, *args, **kwargs):
    name = data.get("name")
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    address_book.delete_record(name=key)
    return f"Contact {key} successfully removed"


@input_error
def delete_phone(data, *args, **kwargs):
    name = data.get("name")
    phone_number = data.get("delete phone")
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    if not number_checker(phone_number):
        raise PhoneDoesNotExistError
    address_book[key].delete_phone(phone=phone_number)
    return f"{key}'s {phone_number} phone number successfully removed"


@input_error
def delete_email(data, *args, **kwargs):
    name = data.get("name")
    email = data.get("delete email")
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    if not mail_checker(email):
        raise EmailDoesNotExistError
    address_book[key].delete_email(email=email)
    return f"{key}'s {email} email successfully removed"


@input_error
def delete_birthday(data, *args, **kwargs):
    name = data.get("name")
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    if address_book[key].birthday.value:
        address_book[key].birthday.var = None
        return f"Birth date for {key}'s contact successfully removed"
    else:
        return f"Contact {key} had no set birth date anyway"


@input_error
def birthday_to(data, *args, **kwargs):
    days = int(data)
    list_of_matches = []
    for i in address_book.values():
        if i.days_to_birthday() == days:
            list_of_matches.append(i.name.value)
    val = f"Contacts with birth in {days} days:\n" + '\n'.join(list_of_matches)
    return val if bool(list_of_matches) else f"No contacts found with birth in {days} days"


@input_error
def search(data, *args, **kwargs):
    if list(data.keys())[0] == "name":
        unpacked_data = data.get("name")
        results = address_book.search(name=unpacked_data)
    elif list(data.keys())[0] == "phone":
        unpacked_data = data.get("phone")
        results = address_book.search(phone=unpacked_data)
    elif list(data.keys())[0] == "email":
        unpacked_data = data.get("email")
        results = address_book.search(email=unpacked_data)
    else:
        raise SearchValueError
    con = '\n' + f"Search results for '{unpacked_data}':" + '\n'
    b = []
    for j in results:
        length = max([len(j.name.value) for j in results])
        a = f"{j.name.value: >{length}}: " \
            f"Phone(s): {', '.join([k.value for k in j.phones]) if j.phones else 'No data'} " \
            f"Email(s): {', '.join([k.value for k in j.emails]) if j.emails else 'No data'}"
        b.append(a)
    con += '\n'.join(b)
    return con


@input_error
def show_user(name, *args, **kwargs):
    key = name.capitalize()
    if key not in address_book:
        raise NoNameError
    res = ""
    n = f"Name: {address_book[key].name.value}"
    p = f"Phone(s): {', '.join([k.value for k in address_book[key].phones]) if address_book[key].phones else 'No data'}"
    e = f"Email(s): {', '.join([k.value for k in address_book[key].emails]) if address_book[key].emails else 'No data'}"
    b = f"Birthday: {address_book[key].birthday.value if address_book[key].birthday.value else 'No data'}"
    res += '\n'.join([n, p, e, b])
    return res


# --- no args part ---


@input_error
def show_all(*args, **kwargs):
    num_lines_in_page = 10
    res = []
    num_page = 0
    if not bool(address_book):
        return "Address book is empty"
    for i in address_book.iterator(num_lines_in_page):
        num_page += 1
        longest_name = max([len(names) for names in i])
        write_num_page = f"page {str(num_page)}"

        page = ("\n".join([f"{str(contact.name.value):<{longest_name}} -> " +
                        (", ".join([i.value for i in contact.phones] if len(contact.phones) > 0
                                   else ['(No phone numbers)']))
                        for contact in i.values()]))

        res.append(page + f"\n{write_num_page:_^{longest_name * 2 + 4}}")

    return "\n\n".join(res)


def info(*args, **kwargs):
    f = "Shows a list of contacts whose birthday is the specified number of days from the current date"
    s = [
        "\n"
        "List of commands:\n",
        "|{:.^30}|{:.^99}|".format("Command name", "Description"),
        "|{:-^30}|{:-^99}|".format("help, info", "Show this page"),
        "|{:-^30}|{:-^99}|".format("add", "Add something in address book"),
        "|{:-^30}|{:-^99}|".format("change", "Change something in address book"),
        "|{:-^30}|{:-^99}|".format("delete", "Delete something from address book"),
        "|{:-^30}|{:-^99}|".format("search by", "Search in the address book"),
        "|{:-^30}|{:-^99}|".format("birthday info", f),
        "|{:-^30}|{:-^99}|".format("show user", "Shows all contact info"),
        "|{:-^30}|{:-^99}|".format("show all", "Show contact list"),
        "|{:-^30}|{:-^99}|".format("bye, close, exit, good bye", "Exit address book"),
        "\n"
    ]
    return "\n".join(s)
    pass


def close(*args, **kwargs):
    sys.exit("Good bye!")


# --- other funcs part ---


def universal_checker(data, type_of_data):
    if re.search(r"name", type_of_data):
        if re.fullmatch(r"[a-zA-Z][a-zA-Z.]+", data):
            return True
        else:
            return False

    elif re.search(r"phone", type_of_data):
        if re.fullmatch(r"\+?\d{1,15}", data):
            return True
        else:
            return False

    elif re.search(r"birthday", type_of_data):
        if re.fullmatch(r"(?:[0-2]\d|3[0-1])\.(?:0\d|1[0-2])\.\d{4}$", data):
            if datetime.strptime(data, "%d.%m.%Y").date() > datetime.now().date():
                return False
            return True
        else:
            return False

    elif re.search(r"email", type_of_data):
        if re.fullmatch(r"[\w.%-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}", data):
            return True
        else:
            return False


def number_checker(num):
    flag = False
    for v in address_book.values():
        for i in v.phones:
            if i.value == num:
                flag = True
                break
    return flag


def mail_checker(mail):
    flag = False
    for v in address_book.values():
        for i in v.emails:
            if i.value == mail:
                flag = True
                break
    return flag


def normalize_phone(number):
    num = re.sub(r'\+', '', number)
    return num


# @input_error
def main():
    """Основна функція, в кій виконується програма"""
    print('Load complete\n')
    if not os.path.exists("data"):
        os.mkdir("data")
    """Дістаємо із файлу данні, та записуємо в адресну книгу"""
    if bool(sorted(Path(os.getcwd()).glob("data/AB.pickle"))):
        if os.stat("data/AB.pickle").st_size:
            with open("data/AB.pickle", 'rb') as file:
                unpacked = pickle.load(file)
                address_book.update(unpacked)
    else:
        with open("data/AB.pickle", 'wb') as file:
            pass

    print("\n-- To see existing commands, type <help> or <info> --")

    """Змінні для реалізації логіки повернення до минулого кроку"""
    first_command = None
    second_command = None

    """Запускаємо основний цикл"""
    while True:

        """Якщо перша команда не збережена, то записуємо інпут від користувача"""
        if first_command is None:
            print("\nWrite the command")
            first_command = input(">>>").lower()

        """
        Якщо користувач ввів "back", то ми перевіряємо чи імпортована ця программа.
        Якщо вона імпортована то ми повертаємось до вибору програм, а якщо не імпортована, то дія неможлива.
        В іншому випадку перевіряємо введену команду на правильність.
        Обнуляємо запис команди перед перезапуском циклу
        """
        if first_command == "back":
            if __name__ == "__main__":
                print("No other software was found!")
                first_command = None
                continue
            else:
                break
        elif first_command not in dict_of_keys:
            print("Wrong first command!")
            first_command = None
            continue

        """
        Якщо введена команда змінює записну книгу, то ми виконуємо наступні дії:
        Інакше ми просто викликаємо потрібну функцію та обнуляємо введену першу команду
        """
        if first_command == "add" or \
                first_command == "change" or \
                first_command == "delete" or \
                first_command == "search by":

            used_dict_of_command = dict_of_keys[first_command]

            """Якщо друга команда не збережена, то записуємо інпут від користувача"""
            if second_command is None:
                print(f"\nWhat do you want to {first_command}?\n"
                      f"<{', '.join([i for i in used_dict_of_command.keys()])}> (select one option)")
                second_command = normalize_phone(input(">>>").lower())

            if second_command in dict_of_keys and dict_of_keys[second_command] == close:
                if __name__ != "__main__":
                    break
                else:
                    close()

            """
            Якщо користувач ввів "back", то ми обнуляємо запис "back" другої команди,
                а також першу для запису іншої команди. Оновлюємо цикл.
            Якщо користувач ввів команду із загального словника, то ми перезаписуємо її в першу команду,
                а другу обнуляємо і перезапускаємо основний цикл
            В іншому випадку перевіряємо введену команду на правильність.
            """
            if second_command == "back":
                first_command = None
                second_command = None
                continue
            elif second_command in dict_of_keys:
                first_command = second_command
                second_command = None
                continue
            elif second_command not in used_dict_of_command:
                print("Wrong second command!")
                second_command = None
                continue

            """Копіюємо значення запису, щоб не змінити його у подальшому в оригінальному словнику"""
            value_of_used_dict = used_dict_of_command[second_command][:]

            """
            Створюємо допоміжні змінні:
            <is_back> - показує чи ввів користувач "back"
            <counter> - це лічильник для циклу
            <all_field> - це список із ключів словника
            """
            is_back = False
            counter = 0
            all_field = [i for i in value_of_used_dict[1]]

            """Створюємо допоміжний цикл, який йде поки <counter> не перевищить кількість записів словника"""
            while counter < len(value_of_used_dict[1]):
                """Записуємо в змінну поточне ім'я із списку <all_field> за допомогою <counter>"""
                name_field = all_field[counter]

                """Просимо ввести необхідні данні і зберігаємо іх в змінній"""
                print(f"\nEnter the {name_field}")
                input_str = normalize_phone(input(">>>"))

                """Якщо користувач ввів "back", то ми вказуємо це в змінній <is_back> і зупиняємо цикл"""
                if input_str.lower() == "back":
                    is_back = True
                    break

                """
                Перевіряємо введену команду на правильність і записуємо в відповідне поле словника замість 'None'
                Інакше запускаємо цей же цикл заново (завдяки поки не зміненій <counter>)
                """
                if universal_checker(input_str, name_field):
                    value_of_used_dict[1][name_field] = input_str
                else:
                    print(f"\nIncorrect input {name_field}. Try again:")
                    continue

                """Змінюємо наш лічильник для запису наступного значення в словнику, або припинення циклу"""
                counter += 1

            """Якщо користувач вводив "back", ми обнуляємо другу команду та запускаємо основний цикл заново"""
            if is_back:
                second_command = None
                continue

            """Звертаємось до функції та виводимо результат користувачу"""
            print(f"\n{value_of_used_dict[0](value_of_used_dict[1])}")

            """Записуємо оновлену адресну книгу в файл"""
            with open("data/AB.pickle", 'wb') as file:
                pickle.dump(address_book, file)

            """Обнуляємо всі записані команді для нового, 'пустого' циклу"""
            first_command = None
            second_command = None
        elif first_command == "birthday info" or first_command == "show user":

            print(f"\nEnter the name of user") if first_command == "show user" else print(f"\nEnter the date")
            second_command = normalize_phone(input(">>>").lower())

            if second_command in dict_of_keys and dict_of_keys[second_command] == close:
                if __name__ != "__main__":
                    break
                else:
                    close()

            if second_command == "back":
                first_command = None
                second_command = None
                continue
            elif second_command in dict_of_keys:
                first_command = second_command
                second_command = None
                continue

            is_back = False

            """Якщо користувач вводив "back", ми обнуляємо другу команду та запускаємо основний цикл заново"""
            if is_back:
                second_command = None
                continue

            """Звертаємось до функції та виводимо результат користувачу"""
            print(f"\n{dict_of_keys[first_command](second_command)}")

            """Обнуляємо всі записані команді для нового, 'пустого' циклу"""
            first_command = None
            second_command = None
        else:
            if dict_of_keys[first_command] == close and __name__ != "__main__":
                break

            print(f"\n{dict_of_keys[first_command]()}")
            first_command = None

    print("Returning to program selection...")


# ---------- End of func part ----------


dict_add = {
    "user": (add_user, {"name": None}),
    "phone": (add_phone, {"name": None, "phone": None}),
    "email": (add_email, {"name": None, "email": None}),
    "birthday": (add_birthday, {"name": None, "birthday": None})
}

dict_change = {
    # "user": (add_user, {"old name": None, "new name": None}),
    "phone": (change_phone, {"name": None, "old phone": None, "new phone": None}),
    "email": (change_email, {"name": None, "old email": None, "new email": None}),
    "birthday": (add_birthday, {"name": None, "birthday": None})
}

dict_delete = {
    "user": (delete_user, {"name": None}),
    "phone": (delete_phone, {"name": None, "delete phone": None}),
    "email": (delete_email, {"name": None, "delete email": None}),
    "birthday": (delete_birthday, {"name": None})
}

dict_search = {
    "user": (search, {"name": None}),
    "phone": (search, {"phone": None}),
    "email": (search, {"email": None}),
}

dict_of_keys = {
    "add": dict_add,
    "change": dict_change,
    "delete": dict_delete,
    "search by": dict_search,
    "birthday info": birthday_to,
    "show user": show_user,
    "show all": show_all,
    "info": info,
    "help": info,
    "good bye": close,
    "close": close,
    "exit": close,
    "bye": close
}

address_book = AddressBook()

if __name__ == "__main__":
    main()
