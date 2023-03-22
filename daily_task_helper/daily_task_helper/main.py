import re
import sys
import os
from .AddressBook import main as main_ab
from .NoteBookByte import main as main_nb
from .NoteBookJson import main as main_nbj
from .Sorter import main as main_s
from .CaloriesCounter import main as main_cc


def main():
    if not os.path.exists("data"):
        os.mkdir("data")
    print(f"\nEnter the name of the program you want to run\n"
          f"<{'>, <'.join([i for i in dict_of_program])}>")

    while True:
        chose_program = input(">>>").lower()
        if chose_program in exit_commands:
            sys.exit("Good bye!")
        elif chose_program == "back":
            print("")
        elif chose_program == "":
            print("\nDo you want to exit? y/n")

            while True:
                confirm_input = input(">>>").lower()
                if confirm_input == "y" or confirm_input == "yes":
                    sys.exit("Good bye!")
                elif confirm_input == "n" or confirm_input == "no":
                    print(f"\nEnter the name of the program you want to run\n"
                          f"<{'>, <'.join([i for i in dict_of_program])}>")
                    break
                else:
                    print("\nEnter 'y'(yes) to exit or 'n'(no) to continue")
            continue

        chose_program = re.sub(" ", "_", chose_program.strip().capitalize())
        if chose_program in dict_of_program:
            dict_of_program[chose_program]()
            print(f"\nYou are back in program selection! Select the program you want to run or type 'exit' to exit\n"
                  f"<{'>, <'.join([i for i in dict_of_program])}>")
        else:
            print(f"\nNo such program exists. Choose from the list below\n"
                  f"Programs available: <{'>, <'.join([i for i in dict_of_program])}>")


dict_of_program = {
    "Address_book": main_ab,
    "Note_book_byte": main_nb,
    "Note_book_json": main_nbj,
    "Sorter": main_s,
    "Calories_counter": main_cc
}

exit_commands = ("good bye", "close", "exit", "bye")

if __name__ == "__main__":
    main()
