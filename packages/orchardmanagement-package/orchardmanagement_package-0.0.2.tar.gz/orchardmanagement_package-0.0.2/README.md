# Orchard Management Package

This repository contains the code for an Orchard Management Package, designed to manage fruit production, inventory, and sales. 
The system is implemented in Python and utilizes the pandas library for data manipulation and matplotlib for plotting.

## Table of Contents
- [Production subpackage]
  - [fruit_info.py]
  - [plantation.py]
- [Management subpackage]
  - [inventory.py]
  - [sales.py]


## Production Subpackage

### fruit_info.py

Module fruit_info defines a hierarchy of fruit classes (subclasses: Apple, Cherry, Peach) that represent various fruits planted in the orchard, and methods to store, modify and manage their information. 

#### Class: Fruit

Class Fruit represents an abstract base class for various fruits planted in an orchard. It includes basic information about fruit, such as fruit variety, size, sweet, sour, taste, price, use, etc
   - variety: The variety of the fruit.
   - size: The size of the fruit. e.g.: medium, big
   - sweet: The sweetness of the fruit e.g. very sweet
   - sour: The sourness of the fruit. e.g. less sour
   - taste: The taste of the fruit, e.g., 'crunchy'.
   - price: The price of the fruit. e.g. 2.99
   - use: The intended use of the fruit. e.g.: "pie"

Method of Fruit:
- `describe() -> string`: 
Returns a brief statement describing the fruit, including size, sourness, sweetness, taste, and use. 
- `get_price() -> float`: 
Returns the price of the fruit.
- `set_price(price)`: 
Sets the price of the fruit.

Abstract Methods in Fruit: 
- `get_type_num() -> int`: 
Abstract method, returns the type number of the fruit.
- `get_available_season(date)`: 
Abstract method, returns the available season of the fruit for the given date.
- `get_type()`: 
Abstract method, returns the type of fruit.

Those three abstract methods will be concretely implemented in subclasses: Apple, Cherry and Peach


#### Subclasses of Fruit:

- Apple: 
Represents an Apple, a specific subclass of Fruit.
    - type_num: The unique type number assigned to all instances of Apple.
    - type: The type of fruit, always set to "apple".
    - season_dict: A dictionary correlating the seasons with the variety of apples allowed for cultivation in the orchard.

- Cherry:
Represents a Cherry, a specific subclass of Fruit.
    - type_num: The unique type number assigned to all instances of Cherry.
    - type: The type of fruit, always set to "cherry".
    - season_dict: A dictionary correlating the seasons with the variety of cherries allowed for cultivation in the orchard.

- Peach:
Represents a Peach, a specific subclass of Fruit.
    - type_num (int): The unique type number assigned to all instances of Peach. always set to 1
    - type (str): The type of fruit, always set to "peach".
    - season_dict (dict): A dictionary correlating the seasons with the variety of peaches
      allowed for cultivation in the orchard.

Methods in subclasses:
- `get_type_num() -> int`: 
Returns the type number of apple/cherry/peach.
- `get_available_season(date)`: 
Returns True if the Peach variety is available in the given date's season, False otherwise. Meanwhile, print at the given season, the Peach variety is in season, out of season, or season has not arrived yet.
- `get_type()`: 
Returns the type of the apple/cherry/peach.

#### Methods:

- `fruit_available_check(date, fruit) -> bool`:
Check if the input fruit is in season for the given date.
- `available_season_fruit(date,fruit_list)`:
Check which fruits are in season for the given date and return a list of fruits.
- `fruit_class_load(file_path) -> list`: 
Loads fruit information from the specified CSV file and returns a list of class instances.
- `get_fruit(type_num, variety, fruits_list) -> Fruit`: 
Retrieves a specific fruit instance based on type number and variety.
- `fruit_information_store(fruit_list, csv_file_path)`: 
Store fruit information in a CSV file for later retrieval.
- `fruit_class_load(fruit_file)`: 
Load fruit information from a file and return a list of Fruit instances.
- `get_fruit(fruit_type_num, variety, fruit_list) -> Fruit`:
Retrieve a unique fruit class based on type number and variety from the given fruit list.
- `add_fruit(fruit_type_num, variety, size, sweet, sour, taste, price, use, fruit_list, fruit_file)`:
Add a new type of fruit record to the list of fruits. The new fruit should not have same type_num and variety with existed fruits.
- `remove_fruit(fruit_type_num, variety, fruit_file)`:
Remove a fruit record from the list of fruits based on the type number and variety.
- `datetime_transfer(date) -> string`:
Help method: Convert 'YYYY-MM-DD' date string to month (MM).
- `file_store(file_path, store_data)`:
Help method: Store data in a CSV file. 
- `file_load(file_path)`:
Help method: Load data from a file. Returns a list of file rows.

### plantation.py

Module plantations contains class and functions related to fruit cultivation regioins. The whole plantation is divided into several regions for different fruit and different use (customer picking/market wholesale.) There is a class region record the basic information and status of regions. Methods including area calculations, region summary report, and data storeage using Dataframes, etc. 

#### Class: Region

Represents a region with specific fruit cultivation information, including region ID, fruit type number, variety, area, and area type.
  - regionId (int): The unique identifier for the region.
  - fruit_type_num (int): The type number of the fruit cultivated in the region.
  - variety (str): The variety of the fruit cultivated in the region.
  - area (float): The area of the region for fruit cultivation.
  - areaType (str): The type of the region, either "market" or "pick".

Methods about Regions:
- `get_area_type()`:
Returns the area type of the region.
- `set_area_type(areaType)`:
Sets the area type of the region. There is only two valid area type: "pick" and "market"
- `get_area()`:
Returns the area of the region.
- `get_fruit(fruit_list)`:
Retrieves the specific fruit instance for the region.
- `region_display(fruit_list)`:
Displays information about the region and the cultivated fruit.

#### Methods:
- `get_region(region_index, region_list)`:
Retrieve a region from the list based on the region ID.
- `set_picking_region(plantingRegion)`:
Set the area type of the planting region to 'pick'
- `set_marketing_region(plantingRegion)`:
Set the area type of the planting region to 'market'
- `area_amount_variety(plantation_list, fruit_type_num, fruit_variety)`:
Get the total planting area for a specific fruit type and variety. Return as a pivot dataframe. 
- `fruit_index_list(plantation_list, fruit_type_num, fruit_variety)`:
Help Method: Get lists of region IDs for a specific fruit type and variety based on area type.
- `region_summary(fruit_list, region_list)`:
Generate a summary DataFrame with picking and marketing area information for each fruit type and variety. It return a data frame containing picking and marketing area information along with region indices.
- `area_summary(fruit_list,region_list)`:
Generate a summary DataFrame with picking and marketing area information for each fruit type. This summary will be used for inventory management
It returns a dataFrame containing only picking and marketing area information.
- `region_saving(plantation_file,region_list)`:
Save region information from a list of Region instances to a DataFrame and store it in a CSV file.
- `region_loading(file_path) -> pd.DataFrame`: 
Loads plantation data from the specified CSV file.
- `region_class_tranfer(data: pd.DataFrame) -> list`: 
Transfers plantation data to a list of class instances.
- `add_region(regionId, fruit_type_num, variety, area, areaType, fruit_list, region_list, planatation_file)`:
Add a new region to the list of regions. This method works for plantation initialization. Since the area of orchard is constant, the number of regions is limited. So this method will only call at the start of main. 


## Management Subpackage

### inventory.py

Handles inventory, remaining production capacity management and simple visualization.

#### Datafiles:
Here are three CSV files: "inventory.csv", "remaining_productivity.csv", and "extra_productivity.csv".   

  - **inventory.csv** : 
  Store the inventory situation, with the latest stock data located at the bottom of the csv table, including historical stock data. 
  - **remaining_productivity.csv** ： 
  Store the estimated remaining productivity. Estimates the yield based on different types of fruits and the corresponding planting areas in orchards first. The estimated yield will be updated as fruits harvested and added to the inventory, or are directly picked and purchased by customers. In case of natural disasters or other events causing a decrease in productivity, adjustments can be made independently.   
  - **extra_productivity.csv** : 
  A supplementary file for anticipated yields. If the total yield exceeds the estimated yield, the surplus is stored in this file to serve as a basis for adjusting future yield estimates.


#### Classes:

- `HistoricalPlotter`: 
A class for plotting historical data related to inventory management and remaining capacity.

  ##### Methods:

  - `__init__(remaining_productivity_file, inventory_file)`: 
  Initializes a HistoricalPlotter instance.
  - `plot_historical_data(fruit_category, file_type)`: 
  Plots historical data based on the specified fruit category and file type.

#### Classes:

- `InventoryManagement`: 
A class for managing inventory, remaining capacity, and extra productivity.

  ##### Methods:

  - `__init__(extra_productivity_file, remaining_productivity_file, inventory_file)`: 
  Initializes an InventoryManagement instance.
  - `load_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]`: 
  Loads data from CSV files (inventory, remaining productivity, extra productivity).
  - `save_data(newdata, filename)`: 
  Saves new data to the specified CSV file.
  - `total_product_estimate() -> str`: 
  Estimates total production based on the number of fruit trees and updates inventory and remaining productivity.
  - `add_inventory(fruit_type, number)`: 
  Adds inventory of a specific fruit type.
  - `add_extra_productivity(fruit_type, number)`: 
  Adds extra productivity of a specific fruit type.
  - `remove_inventory(fruit_type, number)`: 
  Removes inventory of a specific fruit type.
  - `remove_remaining_productivity(fruit_type, number)`: 
  Removes productivity for a specific fruit type.
  - `get_current_inventory() -> pd.DataFrame`: 
  Gets the current inventory status.
  - `get_remaining_productivity() -> pd.DataFrame`: 
  Gets the remaining productivity status.
  - `get_extra_productivity() -> pd.DataFrame`: 
  Gets the extra productivity status.

### sales.py

#### Datafiles:  
  - **orders.csv** : Record all orders in sequence including customer picing and direct sales.


#### Classes:

- `SalesManagement`:  
Manages sales orders and revenue, handle the relation between sales and inventory, and basic visualization.

  ##### Methods:

  - `__init__(inventory_manager, fruit_file, order_file)`: 
  Initializes a SalesManagement instance.
  - `load_data() -> pd.DataFrame`: 
  Loads sales order data from a CSV file.
  - `add_order(sales_type, fruit_variety, weight)`: 
  Adds a new sales order.
  - `order_display()`:
   Displays the sales order data.
  - `revenue_display(variable)`: 
  Displays revenue data based on a specified variable.
  - `revenue_plotter()`: 
  Plots a pie chart of revenue distribution by fruit type.
  - `check_inventory(fruit_variety, weight)`: 
  Checks if selling a specified quantity of fruits is possible.

## Main
Module main.py in the package orchardmanagement is the control panel of the orchard management app. It is combined by fruit_info_operation.py, plantation_operation.py, inventory_operation.py and sales_operation.py
 It provides functionality to view and manage fruit categories, production regions, production inventory, and business orders.

Functions in main.py:
- `basic_choice_select(fruit_file, plantation_file)`: 
Allows the user to make choices to manage the orchard. This is the entry point for orchard employees to access the database. In this context, employees can connect to the database, retrieve information, and perform various tasks related to orchard management.

Functions in Main.py for initialize：
- `file_import`: 
Imports a file using a relative path to create an absolute path
- `fruit_init`: 
Initializes the fruit information for the orchard.
- `plantation_init`: 
Initializes the production regions for the orchard.
- `inventory_init`:
Initialize inventory module
- `sales_init`: 
Initialize sales module
- `clear_csv_file`: 
Initialize files

### Upload

Version 0.0.2 update
Version 0.0.1 orchard_management





