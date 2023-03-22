from datetime import datetime
import os
import pickle
import re
import sys

DATA_FILE = 'data/notepad_data.pickle'


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
        return f"{self.id}"


class EndDate:
    def __init__(self):
        self.end_date = input(
            "Enter date of the end, format(YYYY-MM-DD) or enter nothing: ")
        check = False
        while not check:
            try:
                self.end_date == '' or datetime.strptime(self.end_date, "%Y-%m-%d") == True
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
        note = {"id": id + 1, "title": title.title, "body": body.body,
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
            print(f"No match found")
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
            end_date = datetime.strptime(note["end_date"], "%Y-%m-%d").date() \
                if note["end_date"] is not None else datetime(9999, 1, 1).date()
            if end_date < today:
                self.notes.remove(note)

    def search_by_title_or_body(self):  # перероблю вивід
        searching_text = ""
        matching_notes = []
        while len(searching_text) == 0:
            searching_text = input(
                "Enter the text you want to find in the notes: ")
            if searching_text:
                for note in self.notes:
                    search_in_body = re.search(searching_text, note['body'])
                    search_in_title = re.search(searching_text, note['title'])
                    if search_in_body or search_in_title:
                        first = f"Id: {note['id']}\n" \
                                f"Title: {note['title']}\n" \
                                f"Note:\n{note['body']}\n" \
                                f"End date: {note['end_date'] if note['end_date'] else 'no date data'}"
                        matching_notes.append(first)
            else:
                print("Searching text can't be empty")
        print('\n--------------------------\n'.join(matching_notes))

    def show_notes_with_date_less_today(self):  # перероблю вивід
        matching_notes = []
        for note in self.notes:
            if note['end_date'] is not None and datetime.strptime(note['end_date'],
                                                                  '%Y-%m-%d').date() < datetime.today().date():
                first = f"Id: {note['id']}\n" \
                        f"Title: {note['title']}\n" \
                        f"Note:\n{note['body']}\n" \
                        f"End date: {note['end_date'] if note['end_date'] else 'no date data'}"
                matching_notes.append(first)
        print('\n--------------------------\n'.join(matching_notes)) if matching_notes else print("No matches found")

    def show_all(self):  # перероблю вивід
        mid_list = []
        for note in self.notes:
            first = f"Id: {note['id']}\n" \
                    f"Title: {note['title']}\n" \
                    f"Note:\n{note['body']}\n" \
                    f"End date: {note['end_date'] if note['end_date'] else 'no date data'}"
            mid_list.append(first)
        print('\n--------------------------\n'.join(mid_list))

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
        while not check:
            user_input = input("You have to choose (yes/no): ")
            if user_input.lower() == 'yes' or user_input.lower() == 'no':
                check = True
        if user_input.lower() == 'yes':
            self.save_to_file()
            # sys.exit("Good bye!")
        elif user_input.lower() == 'no':
            print("Changes not saved")
            # sys.exit("Good bye!")
        if __name__ == "__main__":
            sys.exit("Good bye!")


def main():
    if not os.path.exists("data"):
        os.mkdir("data")

    notebook = Notebook()

    @help_wrapper
    def helps():
        for i, command in COMMAND_ID.items():
            print(f"\t{i}: {command}")

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
        print("Datafile is created. Let's add notes to it")

    # ---------------------- Start------------------------------
    print("Hello!")
    helps()

    while True:
        user_input = input(f"\nTo run command enter the ID command: ")
        if user_input in COMMAND_ID.keys():
            if __name__ != "__main__" and user_input == '9':
                notebook.exit()
                break
            COMMANDS_DICT[COMMAND_ID[user_input]]()
        else:
            print(f"No command with id {user_input}, try again")
    print("Returning to program selection...")


if __name__ == "__main__":
    main()
