import src.orchardmanagement_package.production.fruit_info as fruit_info
from datetime import datetime


def fruits_operations(fruit_file):
    """
    Provides operations related to fruit features and seasonal fruit selection.

    1. View fruit features: Display information about various fruit features.
    2. Check seasonal fruit selection: Check which fruits are in season.
    0. Back to main menu: Return to the main menu.

    Usage:
    fruits_operations(fruit_file)
    - 'fruit_file': Path to the CSV file containing fruit information.
    """

    # load fruit_list
    fruits_list = fruit_info.fruit_class_load(fruit_file)

    while True:
        print("Fruit operations: ")
        print("1. View fruit features")
        print("2. Check seasonal fruit selection")
        print("0. Back to main menu")
        fruit_choice_input = input("Please enter operation index here: ")

        try:
            fruit_choice_input = int(fruit_choice_input)
            if fruit_choice_input == 1:
                fruit_check(fruits_list)
            elif fruit_choice_input == 2:
                fruit_seasonal_check(fruits_list)
            elif fruit_choice_input == 0:
                print("Welcome to the Orchard Management Software")
                break
            else:
                print("Invalid operation index")
        except ValueError:
            print("Invalid input, please enter operation index.")


def fruit_check(fruits_list):
    """
    Provides functionality to check and display information about different fruit types.
    """
    apple_list = []
    cherry_list = []
    peach_list = []

    apple_variety = set()
    cherry_variety = set()
    peach_variety = set()

    for fruit in fruits_list:
        if isinstance(fruit, fruit_info.Apple):
            apple_list.append(fruit)
            apple_variety.add(fruit.variety)
        elif isinstance(fruit, fruit_info.Cherry):
            cherry_list.append(fruit)
            cherry_variety.add(fruit.variety)
        else:
            peach_list.append(fruit)
            peach_variety.add(fruit.variety)

    num_input = input("Please enter the index of the fruit you want to search for: 1. Apple, 2. Cherry, 3. Peach :  ")
    try:
        num_input = int(num_input)
        if num_input == 1:
            fruit_variety_check(num_input, apple_variety, fruits_list, "apple")
        elif num_input == 2:
            fruit_variety_check(num_input, cherry_variety, fruits_list, "cherry")
        elif num_input == 3:
            fruit_variety_check(num_input, peach_variety, fruits_list, "peach")
        else:
            print("Invalid fruit index.")
    except ValueError:
        print("Please enter a valid fruit index")


def fruit_variety_check(fruit_type_num, variety_set, fruits_list, fruit_name):
    """
    Displays information about a specific variety of a fruit type.
    """
    variety_input = input(f"Please enter a {fruit_name} variety: {variety_set}:  ")
    curr_date = int(datetime.now().date().strftime("%m"))

    if isinstance(variety_input, str) and variety_input in variety_set:
        fruit_searched = fruit_info.get_fruit(fruit_type_num, variety_input, fruits_list)
        print(f"{variety_input} {fruit_name}: {fruit_searched.describe()}")
        fruit_searched.get_available_season(curr_date)
    else:
        print("Invalid input")


def fruit_seasonal_check(fruits_list):
    """
    Checks and displays available fruits for the current date or a specific date.
    """
    curr_time = datetime.now().date().strftime("%m-%d")
    available_list = fruit_info.available_season_fruit(curr_time, fruits_list)
    if not available_list:
        print(f"Sorry, at date {curr_time}, there is no fruit available now")
    else:
        print(f"Available fruits at {curr_time}: ")
        for fruit_available in available_list:
            print(f"{fruit_available.variety} {fruit_available.get_type()}")
    print("Please enter the date if you want to check seasonal fruit for a specific time. "
          "or enter 'back' to return to the previous menu.")

    date_input = input("Enter datetime with format 'MM-DD' or 'back': ")
    try:
        if date_input == "back":
            fruits_operations()
        date_specific_list = fruit_info.available_season_fruit(date_input, fruits_list)
        if not date_specific_list:
            print(f"Sorry, there is no fruit available on {date_input}")
        else:
            print(f"Available fruits at {date_input}: ")
            for fruit_available in date_specific_list:
                print(f"{fruit_available.variety} {fruit_available.get_type()}")
    except:
        print("Invalid date")