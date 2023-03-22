import json
import os.path
import sys
from colorama import init, Style, Fore
from datetime import datetime


def greeting():
    print("Hello, nice to meet you")


def info():
    s = [
        "\n"
        "|{:-^38}|{:-^99}|".format("Command name", "Descrition"),
        "|{:-^38}|{:-^99}|".format("help", "Show this page"),
        "|{:-^38}|{:-^99}|".format("hello, hi", "Greetings"),
        "|{:-^38}|{:-^99}|".format("add meal",
                                   "Create new meal in everyday dictionary"),
        "|{:-^38}|{:-^99}|".format("create dish",
                                   "Create new dish and add it to the base"),
        "|{:-^38}|{:-^99}|".format("add product",
                                   "Add new product to the base"),
        "|{:-^38}|{:-^99}|".format("show all",
                                   "Show all days(date, total calories and your weight)"),
        "|{:-^38}|{:-^99}|".format("show today's food",
                                   "Show all today's meals"),
        "|{:-^38}|{:-^99}|".format("new day",
                                   "Clean today's meals diary and append general info to the 'diary'"),
        "|{:-^38}|{:-^99}|".format("bye, close, exit, good bye",
                                   "Exit this bot"),
        "\n"
    ]
    print("\n".join(s))


def add_meal():
    food = []
    total = 0
    meal = input("Meal name(For example: Breakfast/Lunch/Dinner)\n>>>").strip().capitalize()

    while True:
        with open("data/caloriesdictionary.json") as fh:
            calories_dict = json.load(fh)
        name = input("Product:\n>>>").strip().capitalize()
        weight = int(input("Weight(grams):\n>>>"))
        cal_per_100 = calories_dict.get(name)

        if calories_dict.get(name) is None:
            co = input(Fore.RED + "We haven't this product in ower base. "
                                  "Click 'Enter' and choose another or type 'back' to return to the main" +
                       Style.RESET_ALL).lower().strip()
            if co == "back":
                break
            else:
                continue

        meal_calories = cal_per_100/100*weight
        food.append(name)
        total += meal_calories
        closer = input("That's all? (yes or no)?\n>>>").strip().lower()

        if closer == "yes":
            with open("data/mealaday.json") as fh:
                file_content = fh.read().strip()
            if not file_content:
                with open("data/mealaday.json", "w") as fh:
                    res = (
                        [{"Time": meal, "Food": food, "Total": int(total)}])
                    json.dump(res, fh, indent=4, ensure_ascii=False)
                    init()
                    print(Fore.GREEN + "Your meal successfully added" +
                          Style.RESET_ALL)
                    break
            else:
                with open("data/mealaday.json") as fh:
                    data = json.load(fh)
                with open("data/mealaday.json", "w") as fh:
                    res = []
                    for i in data:
                        res.append(i)
                    res.append(
                        {"Time": meal, "Food": food, "Total": int(total)})
                    json.dump(res, fh, indent=4, ensure_ascii=False)
                    init()
                    print(Fore.GREEN + "Your meal successfully added" +
                          Style.RESET_ALL)
                    break


def show_today():

    with open("data/mealaday.json") as fh:
        file_in = fh.read().strip()
        if not file_in:
            init()
            print(
                Fore.RED + "You don't add any meals today. Firstly add meal" + Style.RESET_ALL)
        else:
            with open("data/mealaday.json") as f:
                data = json.load(f)
            mn = None
            for i in data:
                mn = i["Time"]
                tc = i["Total"]
                print(f"----------begin of {mn}---------")

                if "Breakfast" in i["Time"]:
                    init()
                    food_list = ", ".join(i["Food"])
                    print(Fore.MAGENTA + f"{food_list}" + Style.RESET_ALL)
                    print(Fore.MAGENTA +
                          f"Total calories: {tc}" + Style.RESET_ALL)
                elif "Lunch" in i["Time"]:
                    init()
                    food_list = ", ".join(i["Food"])
                    print(Fore.CYAN + f"{food_list}" + Style.RESET_ALL)
                    print(Fore.CYAN +
                          f"Total calories: {tc}" + Style.RESET_ALL)
                elif "Dinner" in i["Time"]:
                    init()
                    food_list = ", ".join(i["Food"])
                    print(Fore.YELLOW + f"{food_list}" + Style.RESET_ALL)
                    print(Fore.YELLOW +
                          f"Total calories: {tc}" + Style.RESET_ALL)
                else:
                    food_list = ", ".join(i["Food"])
                    print(f"{food_list}")
                    print(f"Total calories: {tc}")

            print(f"----------end of {mn}----------")
            print("")


def show_diary():
    if not os.path.exists("data/diary.json"):
        with open("data/diary.json", "w") as f:
            pass

    with open("data/diary.json") as fh:
        file_content = fh.read().strip()
        if not file_content:
            print(
                Fore.RED + "Your diary is empty, you need to end at least 1 day" + Style.RESET_ALL)
        else:
            with open("data/diary.json") as file:
                date = json.load(file)
                for i in date:
                    d = i.get("Date")
                    t = i.get("Total")
                    w = i.get("Weight")
                    print(f"--------------{d}----------")
                    print(f"Total calories:{t}")
                    print(f"Your weight:{w}")
                    print("")


def end_of_day():
    with open("data/mealaday.json") as fh:
        weight = input("Add your weight:\n>>>")
        data = json.load(fh)
        total = 0
        for i in data:
            calor = i.get("Total")
            total += calor

    if not os.path.exists("data/diary.json"):
        with open("data/diary.json", "w") as f:
            res = [{"Date": f"{datetime.now().date()}",
                    "Total": total, "Weight": f"{weight}kg"}]
            json.dump(res, f, indent=4, ensure_ascii=False)

    with open("data/diary.json") as file:
        file_content = file.read().strip()

        if not file_content:
            with open("data/diary.json", "w") as f:
                res = [{"Date": f"{datetime.now().date()}",
                        "Total": total, "Weight": f"{weight}kg"}]
                json.dump(res, f, indent=4, ensure_ascii=False)
                init()
                print(Fore.GREEN + "Your day successfully added" + Style.RESET_ALL)
        else:
            with open("data/diary.json") as f:
                file_data = json.load(f)
            with open("data/diary.json", "w") as dh:
                res = []
                for i in file_data:
                    res.append(i)
                res.append({"Date": f"{datetime.now().date()}",
                           "Total": total, "Weight": f"{weight}kg"})
                json.dump(res, dh, indent=4, ensure_ascii=False)
                init()
                print(Fore.GREEN + "Your day successfully added" + Style.RESET_ALL)

        with open("data/mealaday.json", "w") as fh:
            pass


def add_products():
    while True:
        name = input("Name of product:\n>>>").capitalize()
        with open("data/caloriesdictionary.json") as fh:
            calories_dict = json.load(fh)

        if name in calories_dict.keys():
            print("This name already used")
        else:
            cal_per_100 = input("Calories per 100 gr:\n>>>")
            calories_dict.update({name: int(cal_per_100)})
            with open("data/caloriesdictionary.json", "w") as fh:
                json.dump(calories_dict, fh, indent=4,
                          ensure_ascii=False)
            print(Fore.GREEN +
                  f"Product {name} succesfully added" + Style.RESET_ALL)
            break


def create_dish():
    total_calories = 0
    total_weight = 0
    while True:
        with open("data/caloriesdictionary.json") as fh:
            calories_dict = json.load(fh)
        name = input("Name of dish:\n>>>").strip().capitalize()

        if name in calories_dict.keys():
            print(Fore.RED + "This name already used. Try again" + Style.RESET_ALL)
        else:
            while True:
                product = input("Name of product:\n>>>").strip().capitalize()
                weight = int(input("Weight of product(grams):\n>>>"))

                if product in calories_dict:
                    cal_prer_100 = calories_dict.get(product)
                    current = cal_prer_100/100*weight
                    total_calories += current
                    total_weight += weight
                else:
                    print(Fore.RED + "We can't find this product" + Style.RESET_ALL)

                cancel = input("Press 'enter' to choose another product or 'stop' to end and return to the main\n"
                               ">>>").strip().lower()

                if cancel == "stop":
                    if total_weight == 0:
                        break
                    res = total_calories/total_weight*100
                    calories_dict.update({name: int(res)})
                    with open("data/caloriesdictionary.json", "w") as fh:
                        json.dump(calories_dict, fh, indent=4,
                                  ensure_ascii=False)
                    break

            if cancel == "stop":
                init()
                print(Fore.GREEN +
                      f"Dish {name} succesfully added" + Style.RESET_ALL)
                break


def close():
    print("Good Bye)")
    sys.exit(0)


main_dict = {
    "hello": greeting, "hi": greeting, "create dish": create_dish, "add product": add_products, "add meal": add_meal,
    "show today's food": show_today, "show all": show_diary, "new day": end_of_day, "help": info, "info": info,
    "close": close, "exit": close, "good bye": close, "bye": close
}

calories_main_dict = {
    "Apple": 46, "Pork": 254, "Beef": 250, "Orange": 50, "Carrot": 31, "Water": 0, "Oatmeal": 133, "Brandy": 225,
    "Wine": 66, "Vodka": 234, "Gin": 223, "Champagne": 88, "Cola": 40, "Lemonade": 24, "Kvass": 26, "Green tea": 0,
    "Black tea": 0, "Apple juice": 42, "Buckwheat": 137, "Cornflakes": 372, "Cereals": 358, "Champignon": 29,
    "Mayonnaise": 624, "Olive oil": 898, "Sunflower oil": 898, "Butter": 747, "Yoghurt": 87, "Kefir": 51, "Milk": 55,
    "Cream": 209, "Fat cottage cheese": 236, "Bold cottage cheese": 156, "Egg": 153, "Mutton": 201, "Rabbit": 197,
    "Veal": 91, "Turkey": 192, "Duck": 348, "Salmon": 151, "Carp": 95, "Shrimp": 85, "Tuna": 95, "Eggplant": 22,
    "Beans": 59, "Peas": 75, "Cabbage": 33, "Potato": 77, "Green onion": 21, "Onion": 21, "Olives": 111,
    "Bell-pepper": 26, "Radish": 22, "Salad": 15, "Beet": 46, "Tomato": 19, "Cucumber": 16, "Apricot": 44,
    "Pineapple": 49, "Grape": 73, "Cherry": 46, "Pear": 41, "Melon": 34, "Kiwi": 46, "Blackberry": 31,
    "Strawberry": 30, "Lemon": 30, "Mango": 69, "Pamela": 29, "Plum": 41, "Peanut": 555, "Walnut": 662, "Cashew": 647,
    "Almond": 643, "Hazelnut": 701, "Waffles": 425, "Hematogen": 352, "Iris": 384, "Zephyr": 295, "Caramel": 291,
    "Honey": 312, "Marmalade": 289, "Ice cream": 223, "Cookies": 447, "Dark chocolate": 546, "Milk chocolate": 552,
    "White bread": 352, "Loaf": 261, "Lavash": 239, "Brown bread": 201, "Sugar": 400
}


def main():
    print('Load complete\n')
    if not os.path.exists("data"):
        os.mkdir("data")
    if not os.path.exists("data/mealaday.json"):
        with open("data/mealaday.json", "w") as fh:
            pass
    if not os.path.exists("data/caloriesdictionary.json"):
        with open("data/caloriesdictionary.json", "w") as fh:
            json.dump(calories_main_dict, fh, indent=4, ensure_ascii=False)

    print("Hello I'm your calories counter and I will help you with being healthy")

    res = []
    for i in main_dict:
        res.append(i)
    result = "/ ".join(res)

    while True:
        command = input(f"Choose one command from the list: {result}\n>>>").strip().lower()
        if command in main_dict.keys():
            if main_dict[command] == close and __name__ != "__main__":
                break
            com = main_dict.get(command)
            com()
        else:
            print("Command does not exist. Try again")

    print("Returning to program selection...")


if __name__ == '__main__':
    main()
