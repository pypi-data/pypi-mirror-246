import src.orchardmanagement_package.production.fruit_info as fruit_info
import src.orchardmanagement_package.production.plantation as plantation


def region_operations(fruit_file, plantation_file):
    """
    Manage orchard region operations.

    Usage:
    region_operations(fruit_file, plantation_file)
    - 'fruit_file': Path to the file containing fruit information.
    - 'plantation_file': Path to the file containing orchard region information.
    """

    data_region = plantation.region_loading(plantation_file)
    region_list = plantation.region_class_tranfer(data_region)
    fruits_list = fruit_info.fruit_class_load(fruit_file)

    while True:
        print("1. View orchard region report")
        print("2. Switch region type")
        print("0. Back to main menu")

        region_choice_input = input("Please enter your operation index: ")
        try:
            region_choice_input = int(region_choice_input)
            if region_choice_input == 1:
                for region in region_list:
                    region.region_display(fruits_list)
                df_summary = plantation.region_summary(fruits_list, region_list)
                print(df_summary)
            elif region_choice_input == 2:
                region_switch(plantation_file,region_list)
            elif region_choice_input == 0:
                print("Welcome to the Orchard Management Software")
                break
            else:
                print("Invalid operation index")

        except ValueError:
            print("Invalid operation index")


def region_switch(plantation_file, region_list):
    """
    Switch the area_type of an orchard region.
    """
    region_available = []
    for region in region_list:
        region_available.append(region.regionId)
    print(f"Available regions: {region_available}")
    regionId_input = input("Please enter regionId: ")
    try:
        regionId_input = int(regionId_input)
        if regionId_input in region_available:
            region_change = plantation.get_region(regionId_input, region_list)

            type_input = input("Please enter the new region area type, pick or market: ")
            if type_input == "pick":
                plantation.set_picking_region(region_change)
            elif type_input == "market":
                plantation.set_marketing_region(region_change)
            else:
                print("Invalid region area type")
            #save changes
            plantation.region_saving(plantation_file, region_list)
            print("successful save")
        else:
            print("Invalid regionId")
    except ValueError:
        print("Invalid input, please enter a valid regionId.")