import json
from datetime import datetime
import sys
from colorama import init, Style, Fore
from operator import itemgetter
import os.path


file_path = "data/notebook.json"


def greeting():
    print("Hello, nice to meet you")


def add_first_note(title="Without title", note=None, key_words=None, execution=None, filename=file_path):
    title = input("write title \n>>>").upper().strip()
    note = input("write note \n>>>").strip()
    key_words = input(
        "write tags, if more than 1, separate by ';'\n>>>").strip()
    execution = input(
        "write status(Not started/In progress/Completed) \n>>>").strip().capitalize()
    key = key_words.split(";")
    keys = []
    if len(key) > 1:
        for i in key:
            keys.append(i.strip())
    else:
        keys.append(key[0])
    with open(filename, "w") as fh:
        res = []
        res.append({"Title": title, "Date": f"{datetime.now().date()}",
                   "Note": note, "Key words": keys, "Status": execution})
        json.dump(res, fh, indent=4, ensure_ascii=False)


def add_note(title="Without title", note=None, key_words=None, execution=None, filename=file_path):
    title = input("write title \n>>>").strip().upper()
    note = input("write note \n>>>").strip()
    key_words = input(
        "write tags, if more than 1, separate by ';'\n>>>").strip()
    execution = input(
        "write status (Not started/ In progress/ Completed)\n>>>").strip().capitalize()
    key = key_words.split(";")
    keys = []
    if len(key) > 1:
        for i in key:
            keys.append(i.strip())
    else:
        keys.append(key[0])
    with open(filename) as fh:
        res = []
        json_config = json.load(fh)
        for i in json_config:
            res.append(i)
    with open(filename, "w") as fh:
        res.append({"Title": title, "Date": f"{datetime.now().date()}",
                   "Note": note, "Key words": keys, "Status": execution.strip()})
        json.dump(res, fh, indent=4, ensure_ascii=False)


def add_tags(title, key_words, filename=file_path):
    with open(filename, "r") as f:
        data = json.load(f)
        for i in data:
            if i["Title"] == title:
                if len(key_words) > 1:
                    for k in key_words:
                        i["Key words"].append(k)
                else:
                    i["Key words"].append(key_words[0])
    with open(filename, "w") as fh:
        json.dump(data, fh, indent=4, ensure_ascii=False)


def change_tags(filename=file_path):
    while True:
        marker = 0
        inf = input(
            f"write title of tags which you want change\n>>>").strip().upper()
        words = input(
            "Write new tags (if more than 1, separate it by ';')\n>>>").strip()
        keywords = words.split(";")
        with open(filename, "r") as f:
            res = []
            data = json.load(f)
            for i in data:
                if i["Title"] == inf:
                    marker += 1
                    for j in keywords:
                        res.append(j.strip())
            i["Key words"] = res
        with open(filename, "w") as fh:
            json.dump(data, fh, indent=4, ensure_ascii=False)
        if marker == 0:
            if inf.lower() == 'back':
                break
            print(f"Note with the word '{inf}' do not exist. Try again, or write 'back' to return to the main")
        else:
            print(f"Note {inf} successfully changed")
            break


def change_note(filename=file_path):
    while True:
        marker = 0
        inf = input(
            f"write title of note which you want change\n>>>").strip().upper()
        with open(filename, "r") as f:
            data = json.load(f)
            for i in data:
                if i["Title"] == inf:
                    marker += 1
                    i["Note"] = input("New note: \n>>>").strip()
        with open(filename, "w") as fh:
            json.dump(data, fh, indent=4, ensure_ascii=False)
        if marker == 0:
            if inf.lower() == 'back':
                break
            print(f"Note with the word '{inf}' do not exist. Try again, or write 'back' to return to the main")
        else:
            print(f"Note {inf} successfully changed")
            break


def change_title(filename=file_path):
    while True:
        marker = 0
        inf = input(f"write title which you want change\n>>>").strip().upper()
        with open(filename, "r") as f:
            data = json.load(f)
            for i in data:
                if i["Title"] == inf:
                    marker += 1
                    i["Title"] = input("New title: \n>>>").strip().upper()
        with open(filename, "w") as fh:
            json.dump(data, fh, indent=4, ensure_ascii=False)
        if marker == 0:
            if inf.lower() == 'back':
                break
            print(f"Note with the word '{inf}' do not exist. Try again, or write 'back' to return to the main")
        else:
            print(f"Note {inf} successfully changed")
            break


def change_execution(filename=file_path):
    while True:
        marker = 0
        inf = input(
            f"write title of status which you want change\n>>>").strip().upper()
        with open(filename, "r") as f:
            data = json.load(f)
            for i in data:
                if i["Title"] == inf:
                    marker += 1
                    i["Status"] = input(
                        "Choose one: Not started/ In progress/ Completed\n>>>").strip().capitalize()
        with open(filename, "w") as fh:
            json.dump(data, fh, indent=4, ensure_ascii=False)
        if marker == 0:
            if inf.lower() == 'back':
                break
            print(f"Note with the word '{inf}' do not exist. Try again, or write 'back' to return to the main")
        else:
            print(f"Note {inf} successfully changed")
            break


def delete(filename=file_path):
    while True:
        title = input("Which title you want delete?\n>>>").strip().upper()
        with open(filename, "r") as f:
            data = json.load(f)
            with open(filename, "w") as fh:
                marker = 0
                for i in data:
                    if i["Title"] == title:
                        marker += 1
                        k = data.remove(i)
                json.dump(data, fh, indent=4, ensure_ascii=False)
            if marker == 0:
                if title.lower() == 'back':
                    break
                print(f"Note with the word '{title}' does not exist. Try again, or write 'back' to return to the main")
            else:
                print(f"Note {title} successfully deleted")
                break


def tag_sorter():
    filename = file_path
    with open(filename) as fh:
        data = json.load(fh)
        key_list = []
        res = []
        for i in data:
            key_list += i.get("Key words")
            key_set = set(key_list)
        for tag in key_set:
            tag_list = [f"{tag}:"]
            for j in data:
                for tags in j["Key words"]:
                    if tags == tag:
                        tag_list.append(j)
            res.append(tag_list)
    for i in res:
        print(f"---------------{i[0]}---------------")
        printing(i[1])


def date_sorter():
    filename = file_path
    with open(filename) as fh:
        data = json.load(fh)
        a = sorted(data, key=itemgetter("Date"))
        while True:
            rev = input("From first or from last note?\n>>>").lower().strip()
            if rev == "first":
                for i in a:
                    printing(i)
                break
            elif rev == "last":
                a.reverse()
                for i in a:
                    printing(i)
                break
            else:
                if rev == 'back':
                    break
                print(
                    "Incorrect command. Try again")


def find():
    filename = file_path
    while True:
        info = input("What you want to find?\n>>>").strip()
        marker = 0
        with open(filename, "r") as f:
            date = json.load(f)
        for i in date:
            for values in i.values():
                if type(values) == str:
                    if values == info:
                        marker += 1
                        printing(i)
                elif type(values) == list:
                    for name in values:
                        if name == info:
                            marker += 1
                            printing(i)

        if marker == 0:
            if info == 'back':
                break
            print(f"Note with the word '{info}' do not exist. Try again")
        else:
            break


def info():
    s = [
        "\n"
        "List of commands:\n",
        "|{:-^35}|{:-^50}|".format("Command name", "Description"),
        "|{:-^35}|{:-^50}|".format("help", "Show this page"),
        "|{:-^35}|{:-^50}|".format("hello, hi", "Greetings"),
        "|{:-^35}|{:-^50}|".format("add(note/tags)",
                                   "Create a note or add tags to note"),
        "|{:-^35}|{:-^50}|".format("change(title/note/key words/status)",
                                   "Change title or note or key word or status"),
        "|{:-^35}|{:-^50}|".format("delete",
                                   "Deletes a note with chosen title'"),
        "|{:-^35}|{:-^50}|".format("show all",
                                   "Show all notes"),
        "|{:-^35}|{:-^50}|".format("find",
                                   "Finds a notes with the 'word'"),
        "|{:-^35}|{:-^50}|".format("sort(title/date)",
                                   "Print sorted notes by date or titles"),
        "|{:-^35}|{:-^50}|".format("bye, close, exit, good bye",
                                   "Exit this bot"),
        "\n"
    ]
    print("\n".join(s))


def show_all():
    filename = file_path
    with open(filename, "r") as f:
        data = json.load(f)
        for i in data:
            printing(i)


def close():
    # print("Good Bye)")
    # sys.exit(0)
    sys.exit("Good bye!")


def printing(i):
    print("----------begin of note----------")
    if i["Status"] in dict_execution.keys():
        init()
        col = i.get("Status")
        color = dict_execution.get(col)
        print(color)
        print(color + i["Title"], i["Date"] + Style.RESET_ALL)
        if i["Note"] != "":
            print(color + i["Note"] + Style.RESET_ALL)
        if i["Key words"] != []:
            if len(i["Key words"]) > 1:
                print(color + ",".join(i["Key words"]) + Style.RESET_ALL)
            else:
                print(color + "".join(i["Key words"]) + Style.RESET_ALL)
    else:
        print(i["Title"], i["Date"])
        if i["Note"] != "":
            print(i["Note"])
        if i["Key words"] != []:
            if len(i["Key words"]) > 1:
                print(", ".join(i["Key words"]))
            else:
                print(i["Key words"])
    print("----------end of note----------")
    print("")


def main():
    print('Load complete\n')
    if not os.path.exists("data"):
        os.mkdir("data")
    while True:
        if not os.path.exists(file_path):
            print(
                "You haven't got any notes. Create your first note to begin")
            add_first_note()
        with open(file_path) as file:
            file_content = file.read().strip()
            if not file_content:
                print("You haven't got any notes. Create your first note to begin")
                add_first_note()
        print("\nWhat i need to do?")
        command = input(">>>").lower().strip()
        if command in main_dict.keys():
            if command == "close" or command == "bye" or command == "good bye" or command == "exit":
                if __name__ != "__main__":
                    break
                else:
                    close()
            if command == "add":
                while True:
                    deep_command = input(
                        "What you want to add, \"note\" or \"tag\" \n>>>").lower().strip()
                    if deep_command == "note":
                        add_note()
                        break
                    elif deep_command == "tag":
                        title = input("write title \n>>>").strip().upper()
                        key_words = input(
                            "write key words, separate by';'\n >>>").split(";")
                        add_tags(title, key_words)
                        break
                    else:
                        if deep_command == 'back':
                            break
                        print("Incorrect command. Try again")

            elif command == "change":
                list_dict = "/".join([i for i in dict_change])
                while True:
                    deep_command = input(
                        f"Choose what you want to change (one option) '{list_dict}'\n>>>").lower().strip()
                    if deep_command in dict_change.keys():
                        com = dict_change.get(deep_command)
                        com()
                        break
                    else:
                        if deep_command == 'back':
                            break
                        print("Incorrect command. Try again")

            elif command == "sort":
                while True:
                    criterion = input(
                        "Choose the criterion(tags/date) \n>>>").strip().lower()
                    if criterion in dict_sorted.keys():
                        com = dict_sorted.get(criterion)
                        com()
                        break
                    else:
                        if criterion == 'back':
                            break
                        print("Incorrect command. Try again")
            else:
                com = main_dict.get(command)
                com()
        else:
            print(
                "This command does not exist. Type 'help' for find information about commands")
    print("Returning to program selection...")


dict_execution = {
    "Not started": Fore.RED,
    "In progress": Fore.YELLOW,
    "Completed": Fore.GREEN
}

dict_add = {
    "note": add_note,
    "tag": add_tags
}

dict_change = {
    "title": change_title,
    "note": change_note,
    "tags": change_tags,
    "status": change_execution
}

dict_sorted = {
    "tags": tag_sorter,
    "date": date_sorter
}

main_dict = {
    "hi": greeting,
    "hello": greeting,
    "add": dict_add,
    "change": dict_change,
    "delete": delete,
    "show all": show_all,
    "find": find,
    "help": info,
    "info": info,
    "good bye": close,
    "close": close,
    "exit": close,
    "bye": close,
    "sort": dict_sorted
}

if __name__ == "__main__":
    main()
