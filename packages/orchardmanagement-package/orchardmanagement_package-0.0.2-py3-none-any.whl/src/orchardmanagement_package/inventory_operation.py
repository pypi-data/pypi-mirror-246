from src.orchardmanagement_package import management as inventory


def inventory_operator(extra_productivity_file, remaining_productivity_file, inventory_file):
    # Instantiate the InventoryManagement class
    inventory_manager = inventory.InventoryManagement(extra_productivity_file, remaining_productivity_file, inventory_file)
    plotter = inventory.HistoricalPlotter(remaining_productivity_file, inventory_file)

    while True:
        print("Inventory Operations:")
        print("1. View Current Inventory")
        print("2. View Remaining Productivity")
        print("3. Add Inventory")
        print("4. Remove Inventory")
        print("5. View production more than estimated")
        print("6. View the plot of inventory history data ")
        print("0. Back to Main Menu")

        operation_choice = input("Please enter operation index here: ")

        try:
            operation_choice = int(operation_choice)
            if operation_choice == 1:
                inventory_manager.get_current_inventory()
            elif operation_choice == 2:
                inventory_manager.get_remaining_productivity()
            elif operation_choice == 3:
                fruit_type = input(
                    "Enter fruit type(choose from Ambrosia,Gala,Honeycrisp,Lapins,Sweetheart,Skeena,Redhaven,Elberta,Cresthaven): ")
                quantity = int(input("Enter quantity to add: "))
                inventory_manager.add_inventory(fruit_type, quantity)
            elif operation_choice == 4:
                fruit_type = input("Enter fruit type(choose from Ambrosia,Gala,Honeycrisp,Lapins,Sweetheart,Skeena,Redhaven,Elberta,Cresthaven):")
                quantity = int(input("Enter quantity to remove: "))
                inventory_manager.remove_inventory(fruit_type, quantity)
            elif operation_choice == 5:
                inventory_manager.get_extra_productivity()
            elif operation_choice == 6:
                fruit_type = int(input("Enter fruit type(1-Apple, 2-Cherry, 3-Peach):"))
                file_type = int(input("Enter 1 for inventory and 2 for remaining capacity:"))
                plotter.plot_historical_data(fruit_type, file_type)
            elif operation_choice == 0:
                print("Back to the Main Menu.")
                break
            else:
                print("Invalid operation index.")
        except ValueError:
            print("Invalid input, please enter operation index.")
