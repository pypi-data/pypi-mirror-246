import src.orchardmanagement_package.production.fruit_info as fruit_info

"""
This module is a test.py for fruit_info
"""


a1 = fruit_info.Apple("Ambrosia", "big", "very sweet", "less sour", "crunchy", 1.2, "pie")
p1 = fruit_info.Peach("Elberta", "big", "very sweet", "less sour", "crunchy", 1.2, "pie")
c1 = fruit_info.Cherry("Lapins", "small", "median sweet", "median sour", "soft", 2.99, "cans")

print(a1.describe())
print(c1.describe())
print(p1.describe())
"""
expect output: 
big, less sour, very sweet, crunchy.It is good for pie
small, median sour, median sweet, soft.It is good for cans
big, less sour, very sweet, crunchy.It is good for pie
"""

print(a1.get_type_num())
print(c1.get_type_num())
print(p1.get_type_num())

"""
expect output:
1
2
3
"""

print(a1.get_price())
"""
expect output:
1.2
"""

fruit_info.fruit_available_check("9-10", a1)
fruit_info.fruit_available_check("9-10", c1)
fruit_info.fruit_available_check("9-10", p1)
"""
expect output:

Ambrosia Apple is available now
Sorry, Lapins Cherry season has ended.
Elberta Peach is available now
"""
fruit_list = [a1, p1, c1]
fruit_available_list = fruit_info.available_season_fruit("9-10", fruit_list)
for f in fruit_available_list:
    print(f)
"""
big, less sour, very sweet, crunchy.It is good for pie
big, less sour, very sweet, crunchy.It is good for pie
"""

file_path = "fruits_test.csv"
fruit_info.fruit_information_store(fruit_list, file_path)
print(fruit_info.file_load(file_path))
"""
expect output:
[['1', 'Ambrosia', 'big', 'very sweet', 'less sour', 'crunchy', '1.2', 'pie'], 
['3', 'Elberta', 'big', 'very sweet', 'less sour', 'crunchy', '1.2', 'pie'], 
['2', 'Lapins', 'small', 'median sweet', 'median sour', 'soft', '2.99', 'cans']]
"""

fruit_list = fruit_info.fruit_class_load(file_path)
for i in fruit_list:
    print(i.describe())
"""
big, less sour, very sweet, crunchy.It is good for pie
big, less sour, very sweet, crunchy.It is good for pie
small, median sour, median sweet, soft.It is good for cans
"""
fruit_searched = fruit_info.get_fruit(1, "Ambrosia", fruit_list)
print(fruit_searched.describe())
"""
expect output:
big, less sour, very sweet, crunchy.It is good for pie
"""

fruit_info.add_fruit(1, "Gala", "big", "very sweet", "less sour", "crunchy", 1.2, "pie", file_path)
fruit_info.remove_fruit(1, "Gala", file_path)
fruit_info.add_fruit(1, "Ambrosia", "big", "very sweet", "less sour", "crunchy", 1.2, "pie", file_path)
"""
expect output:

(success and no response)
(success and no response)
Fail to add new fruit, the input fruit is already exist
"""






