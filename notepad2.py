from datetime import datetime
import pickle
import re
import sys


DATA_FILE = 'notepad_data.dat'


def choice_answer_delete(func):
    def inner(*args, **kwargs):
        user_input = input(
            'Are you sure you want to delete?(yes/no): ')
        if user_input.lower() == 'yes':
            func(*args, **kwargs)
            print(f"Delete complited")
        elif user_input.lower() == 'no':
            print(f"Delete canceled")
        else:
            print(f"Incorrect command. You have to enter comand 'yes' or 'no'")
            return inner(*args, **kwargs)
    return inner


def help_wrapper(func):
    def inner(*args, **kwargs):
        print(f"Here is the list of all commands: \n")
        func(*args, **kwargs)

    return inner


def id_wrapper(func):
    def inner(*args, **kwargs):
        try:
            int(func(*args, **kwargs))
        except:
            print(f"ID must be integer, please enter the correct value.")
            func(*args, **kwargs)
    return inner


def title_body_wrapper(func):
    def inner(*args, **kwargs):
        while len(func(*args, **kwargs)) == 0:
            print(f"Title or note text can't be empty, please enter correct data.")
    return inner


class Title:
    @title_body_wrapper
    def __init__(self):
        self.title = input("Enter the title: ")
        return f"{self.title}"


class Body:
    @title_body_wrapper
    def __init__(self):
        self.body = input("Enter the note text: ")
        return f"{self.body}"


class Id:
    @id_wrapper
    def __init__(self):
        self.id = input("Enter the note ID: ")
        return F"{self.id}"


class EndDate:
    def __init__(self):
        self.end_date = input(
            "Enter date of the end, format(YYYY-MM-DD) or enter nothing: ")
        check = False
        while check == False:
            try:
                self.end_date == '' or datetime.strptime(
                    self.end_date, "%Y-%m-%d") == True
                self.end_date = None if self.end_date == '' else self.end_date
                check = True
            except ValueError:
                self.end_date = input(
                    "Enter date of the end, format(YYYY-MM-DD): ")


class Notebook:
    def __init__(self):
        self.notes = []

    def add_note(self):
        id = 0
        for d in self.notes:
            if d["id"] > id:
                id = d["id"]
        title = Title()
        body = Body()
        end_date = EndDate()
        note = {"id": id+1, "title": title.title, "body": body.body,
                "end_date": end_date.end_date}
        self.notes.append(note)

    def change_note_body_by_title(self):
        matching_notes = []
        title = Title()
        searching_text = title.title
        if searching_text:
            for note in self.notes:
                find = re.search(title.title, note["title"])
                if find:
                    matching_notes.append(note)
        else:
            while len(searching_text) == 0:
                searching_text = input(
                    "Searching text can't be empty, please enter the text for search: ")
        if len(matching_notes) == 0:
            print(f"NO match found")
        else:
            print(
                f"All notes with searching text in title:\n{matching_notes}\n")
            user_input = input(f"Enter ID one of note for edit: ")
            if int(user_input) not in list(note["id"] for note in matching_notes):
                while int(user_input) not in list(note["id"] for note in matching_notes):
                    user_input = input(
                        f"Incorrect note ID, please enter ID from list: ")
            else:
                for note in self.notes:
                    if int(user_input) == note["id"]:
                        print(f"Old note:\n{note}")
                        new_body = Body()
                        new_date = EndDate()
                        note["body"] = new_body.body
                        note["end_date"] = new_date.end_date

    def delete_note_by_id(self):
        user_input = Id().id

        @choice_answer_delete
        def delete():
            for note in self.notes:
                if note['id'] == int(user_input):
                    self.notes.remove(note)
            return self.notes
        return delete()

    @choice_answer_delete
    def delete_all_note_with_old_dates(self):
        today = datetime.today().date()
        for note in self.notes:
            end_date = datetime.strptime(
                note["end_date"], "%Y-%m-%d").date() if note["end_date"] != None else datetime(9999, 1, 1).date()
            if end_date < today:
                self.notes.remove(note)
            break

    def search_by_title_or_body(self):
        searching_text = input(
            "Enter the text you want to find in the notes: ")
        matching_notes = []
        if searching_text:
            for note in self.notes:
                search_in_body = re.search(searching_text, note['body'])
                search_in_title = re.search(searching_text, note['title'])
                if search_in_body or search_in_title:
                    matching_notes.append(note)
        else:
            while len(searching_text) == 0:
                searching_text = input(
                    "Searching text can't be empty, please enter the text for search: ")
        print(matching_notes)

    def show_notes_with_date_less_today(self):
        matching_notes = []
        for note in self.notes:
            if note['end_date'] != None and datetime.strptime(note['end_date'], '%Y-%m-%d').date() < datetime.today().date():
                matching_notes.append(note)
        print(matching_notes)

    def show_all(self):
        for note in self.notes:
            print(note)

    def save_to_file(self):
        with open(DATA_FILE, "wb") as fh:
            pickle.dump(self.notes, fh)
        print(f"Saving complete")

    def load_from_file(self):
        with open(DATA_FILE, "rb") as fh:
            data = pickle.load(fh)
            for note in data:
                self.notes.append(note)

    def create_file(self):
        with open(DATA_FILE, 'wb') as fh:
            pass

    def exit(self):
        check = False
        user_input = input("Save changes before exit?(yes/no): ")
        if user_input.lower() == 'yes' or user_input.lower() == 'no':
            check = True
        while check == False:
            user_input = input("You have to choose (yes/no): ")
            if user_input.lower() == 'yes' or user_input.lower() == 'no':
                check = True
        if user_input.lower() == 'yes':
            self.save_to_file()
            sys.exit("Good bye!")
        elif user_input.lower() == 'no':
            print("Changes not saved")
            sys.exit("Good bye!")


def main():
    notebook = Notebook()

    @help_wrapper
    def helps():
        for id, command in COMMAND_ID.items():
            print(f"\t{id}: {command}")

    COMMAND_ID = {"0": "help(list of all commands)",
                  "1": "add new note",
                  "2": "change note text",
                  "3": "delete note by id",
                  "4": "delete all notes with expired date",
                  "5": "search notes by title or text",
                  "6": "show all notes with end date less then today",
                  "7": "show all notes",
                  "8": "save changes",
                  "9": "exit",
                  }

    COMMANDS_DICT = {"help(list of all commands)": helps,
                     "add new note": notebook.add_note,
                     "change note text": notebook.change_note_body_by_title,
                     "delete note by id": notebook.delete_note_by_id,
                     "delete all notes with expired date": notebook.delete_all_note_with_old_dates,
                     "search notes by title or text": notebook.search_by_title_or_body,
                     "show all notes with end date less then today": notebook.show_notes_with_date_less_today,
                     "show all notes": notebook.show_all,
                     "save changes": notebook.save_to_file,
                     "exit": notebook.exit,
                     }

    try:
        notebook.load_from_file()
        print('Load complete\n')
    except EOFError:
        print('The file is empty')
    except FileNotFoundError:
        notebook.create_file()
        print("Datafile is created. Let's add notes to it.")

    # ---------------------- Start------------------------------
    print("Hello!")
    helps()

    while True:
        user_input = input(f"\nTo run command enter the ID command: ")
        if user_input in COMMAND_ID.keys():
            COMMANDS_DICT[COMMAND_ID[user_input]]()


if __name__ == "__main__":
    main()


# n1 = Notebook()
# n1.add_note('uuoo', '11111edcvfr', '2025-03-10')
# n1.save_to_file('test.dat')
# n1.load_from_file('test.dat')
# n2 = Notebook()
# n2.load_from_file('test.dat')
# n2.add_note('ffff', 'poiuytre', '5555-08-12')
# n2.save_to_file('test.dat')
# n3 = Notebook()
# n3.load_from_file('test.dat')
# n3.add_note('ppp', 're', '1955-08-18')
# n3.save_to_file('test.dat')
# n4 = Notebook()
# n4.load_from_file('test.dat')
# n4.show_all()
# n = Notebook()
# n.load_from_file()
# n.show_all()
# n.add_note()
# n.show_all()
# print(n.search_by_title_or_body())
