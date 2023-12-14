import csv
from datetime import datetime
from abc import ABCMeta, abstractmethod
"""
Module Description:

This module defines a hierarchy of fruit classes (subclasses: Apple, Cherry, Peach) that represent various fruits
planted in an orchard. It includes functionality for checking fruit availability, storing and loading
fruit information to and from CSV files, and retrieving specific fruit instances based on type number
and variety.

Please see the docstrings within each function and class for more detailed information.
"""


class Fruit(metaclass=ABCMeta):
    """
    Represents an abstract base class for various fruits planted in orchard.
    It has three subclasses: Apple, Cherry and Peach

    Note:
    This is an abstract base class, and subclasses are required to implement get_type_num, get_available_season,
         and get_type methods.
    The `variety` parameter must be one of the varieties stored in the `season_dict` of the subclass.
    No two fruit classes in the orchard are allowed to have same type number and variety.
    """

    def __init__(self, variety, size, sweet, sour, taste, price, use):
        """
        Initializes an instance of Fruit.

        Parameters:
        - variety (str): The variety of the fruit.
        - size (str): The size of the fruit. e.g: medium, big
        - sweet (float): The sweetness of the fruit e.g. very sweet
        - sour (float): The sourness of the fruit. e.g. less sour
        - taste (str): The taste of the fruit, e.g., 'crunchy'.
        - price (float): The price of the fruit. e.g 2.99
        - use (str): The intended use of the fruit. e.g: "pie"
        """
        self.variety = variety
        self.size = size
        self.sweet = sweet
        self.sour = sour
        self.taste = taste
        self.__price = price
        self.use = use

    def describe(self):
        """
        Returns a brief statement describing the fruit, including size, sourness, sweetness, taste, and use.
        """
        describe_sentence = (f"{self.size}, {self.sour}, {self.sweet}, {self.taste}." +
                             f"It is good for {self.use}")
        return describe_sentence

    # def __str__(self):
    #     return Fruit.describe(self)

    def get_price(self):
        """
        Returns the price of the fruit.
        """
        return self.__price


    def set_price(self, price):
        """
        Sets the price of the fruit.
        """
        self.__price = price


    @abstractmethod
    def get_type_num(self):
        """
        Abstract method, returns the type number of the fruit.
        """
        pass

    @abstractmethod
    def get_available_season(self, date):
        """
        Abstract method, returns the available season of the fruit for the given date.
        """
        pass

    @abstractmethod
    def get_type(self):
        """
        Abstract method, returns the type of the fruit.
        """
        pass

class Apple(Fruit):
    """
    Represents an Apple, a specific subclass of Fruit.

    Class Attributes:
    - type_num (int): The unique type number assigned to all instances of Apple. always set to 1
    - type (str): The type of fruit, always set to "apple".
    - season_dict (dict): A dictionary correlating the seasons with the variety of apples
      allowed for cultivation in the orchard.
    """

    type_num = 1
    type = "apple"

    season_dict = {"Ambrosia": [9,10],
                   "Gala": [8,9,10],
                   "Honeycrisp": [9,10]}

    def __init__(self, variety, size, sweet, sour, taste, price, use):
        """
        Initializes an instance of Apple.
        """
        Fruit.__init__(self, variety, size, sweet, sour, taste, price, use)

    def get_type_num(self):
        """
        Returns the unique type number of the Apple. always 1
        """
        return Apple.type_num

    def get_type(self):
        """
        Returns the type of the Apple, always "apple".
        """
        return Apple.type

    def get_available_season(self, date):
        """
        Returns True if the Apple variety is available in the given date's season, False otherwise.
        Meanwhile, print at the given season, the Apple variety is in season, out of season, or
        season has not arrived yet.
        """
        season_list = Apple.season_dict[self.variety]
        if date in season_list:
            print(f"{self.variety} Apple is available now")
            return True
        elif date < min(season_list):
            print(f"Sorry, {self.variety} Apple is not ripe now.")
            return False
        else:
            print(f"Sorry, {self.variety} Apple season has ended.")
            return False


class Cherry(Fruit):
    """
    Represents an Cherry, a specific subclass of Fruit.

    Class Attributes:
    - type_num (int): The unique type number assigned to all instances of Cherry. always set to 2
    - type (str): The type of fruit, always set to "cherry".
    - season_dict (dict): A dictionary correlating the seasons with the variety of cherry
      allowed for cultivation in the orchard.
    """
    type_num = 2
    type = "cherry"

    season_dict = {"Lapins": [6,7],
                   "Sweetheart": [6,7],
                   "Skeena": [7,8]}

    def __init__(self, variety, size, sweet, sour, taste, price, use):
        """
        Initializes an instance of Cherry.
        """
        Fruit.__init__(self, variety, size, sweet, sour, taste, price, use)

    def get_type_num(self):
        """
        Returns the unique type number of the Cherry. always 2
        """
        return Cherry.type_num

    def get_type(self):
        """
        Returns the type of the Apple, always "cherry".
        """
        return Cherry.type

    def get_available_season(self, date):
        """
        Returns True if the Cherry variety is available in the given date's season, False otherwise.
        Meanwhile, print at the given season, the Cherry variety is in season, out of season, or
        season has not arrived yet.
        """

        season_list = Cherry.season_dict[self.variety]
        if date in season_list:
            print(f"{self.variety} Cherry is available now")
            return True
        elif date < min(season_list):
            print(f"Sorry, {self.variety} Cherry is not ripe now.")
            return False
        else:
            print(f"Sorry, {self.variety} Cherry season has ended.")
            return False



class Peach(Fruit):
    """
    Represents an Peach, a specific subclass of Fruit.

    Class Attributes:
    - type_num (int): The unique type number assigned to all instances of Peach. always set to 1
    - type (str): The type of fruit, always set to "peach".
    - season_dict (dict): A dictionary correlating the seasons with the variety of peaches
      allowed for cultivation in the orchard.
    """

    type_num = 3
    type = "peach"

    season_dict = {"Redhaven": [7, 8],
                   "Elberta": [8, 9],
                   "Cresthaven": [8, 9]}

    def __init__(self, variety, size, sweet, sour, taste, price, use):
        """
        Initializes an instance of Apple.
        """
        Fruit.__init__(self, variety, size, sweet, sour, taste, price, use)

    def get_type_num(self):
        """
        Returns the unique type number of the Peach. always 3
        """
        return Peach.type_num

    def get_type(self):
        """
        Returns the type of the Apple, always "peach".
        """
        return Peach.type

    def get_available_season(self, date):
        """
        Returns True if the Peach variety is available in the given date's season, False otherwise.
        Meanwhile, print at the given season, the Peach variety is in season, out of season, or
        season has not arrived yet.
        """
        season_list = Peach.season_dict[self.variety]
        if date in season_list:
            print(f"{self.variety} Peach is available now")
            return True
        elif date < min(season_list):
            print(f"Sorry, {self.variety} Peach is not ripe now.")
            return False
        else:
            print(f"Sorry, {self.variety} Peach season has ended.")
            return False


def datetime_transfer(date):
    """
    Convert 'MM-DD' date string to month (MM).
    """
    try:
        if isinstance(date, str):
            date = datetime.strptime(date, '%m-%d')
        month = date.month
        return month
    except:
        print("Invalid datetime")


def fruit_available_check(date, fruit):
    """Check if the input fruit is in season for the given date."""
    month = datetime_transfer(date)
    return fruit.get_available_season(month)


def available_season_fruit(date,fruit_list):
    """Check which fruits are in season for the given date and return a list of fruit."""
    month = datetime_transfer(date)
    available_list = []
    for f in fruit_list:
        variety = f.variety
        season_list = f.season_dict[variety]
        if month in season_list:
            available_list.append(f)
    return available_list


def file_store(file_path, store_data):
    """Store data in a CSV file."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(store_data)


def fruit_information_store(fruit_list, csv_file_path):
    """Store fruit information in a CSV file for later retrieval."""
    #csv_file_path = "fruits.csv"

    fruit_info_list = []
    for fruit in fruit_list:
        if fruit is not None:
            type_num = fruit.get_type_num()
            variety = fruit.variety
            size = fruit.size
            sweet = fruit.sweet
            sour = fruit.sour
            taste = fruit.taste
            price = round(fruit.get_price(), 2)
            use = fruit.use

            fruit_info = tuple([type_num, variety, size, sweet, sour, taste, price, use])
            fruit_info_list.append(fruit_info)

    file_store(csv_file_path, fruit_info_list)


def file_load(file_path):
    """Helper method: Load data from a file. Returns a list of file rows."""
    file_rows = []
    try:
        with open(file_path, "r") as infile:
            for line in infile:
                line = line.strip(" \n")
                fields = line.split(",")
                for i in range(0, len(fields)):
                    fields[i] = fields[i].strip()
                file_rows.append(fields)

        return file_rows
    except FileNotFoundError:
        print(f"There is no file {file_path}")


def fruit_class_load(fruit_file):
    """Load fruit information from a file and return a list of Fruit instances."""
    try:
        file_rows = file_load(fruit_file)
        fruit_list = []

        if file_rows == [['']]:
            # check if the file exist but empty
            return fruit_list

        for row in file_rows:
            fruit = None
            # title_list = ["type_num", "variety", "size", "sweet", "sour", "taste", "price", "use"]
            type_num = int(row[0])
            variety = row[1]
            size = row[2]
            sweet = row[3]
            sour = row[4]
            taste = row[5]
            price = float(row[6])
            use = row[7]

            if type_num == 1:
                fruit = Apple(variety, size, sweet, sour, taste, price, use)
            elif type_num == 2:
                fruit = Cherry(variety, size, sweet, sour, taste, price, use)
            elif type_num == 3:
                fruit = Peach(variety, size, sweet, sour, taste, price, use)
            else:
                print("These is not a valid production type num, please check your file content")
            fruit_list.append(fruit)
        return fruit_list

    except:
        # check if the file is not exist
        print("None file exist")


def get_fruit(fruit_type_num, variety, fruit_list):
    """Retrieve a unique fruit class based on type number and variety from the given fruit list."""
    for fruit in fruit_list:
        if fruit_type_num == fruit.get_type_num() and variety == fruit.variety:
            return fruit


def add_fruit(fruit_type_num, variety, size, sweet, sour, taste, price, use, fruit_file):
    """
    Add a new type of fruit record to the list of fruits. The new fruit should not have same type_num
    and variety with existed fruits.
    """
    # check there is no same fruit record at first
    fruit_list = fruit_class_load(fruit_file)
    fruit_created = None
    if get_fruit(fruit_type_num, variety, fruit_list) is None:
        if fruit_type_num == Apple.type_num and variety in list(Apple.season_dict.keys()):
            fruit_created = Apple(variety, size, sweet, sour, taste, price, use)
        elif fruit_type_num == Cherry.type_num and variety in list(Cherry.season_dict.keys()):
            fruit_created = Cherry(variety, size, sweet, sour, taste, price, use)
        elif fruit_type_num == Peach.type_num and variety in list(Peach.season_dict.keys()):
            fruit_created = Peach(variety, size, sweet, sour, taste, price, use)
        else:
            print("Invalid input, please enter fruit information with correct type_num and variety")
        fruit_list.append(fruit_created)
        fruit_information_store(fruit_list, fruit_file)
    else:
        print("Fail to add new fruit, the input fruit is already exist")


def remove_fruit(fruit_type_num, variety, fruit_file):
    """
    Remove a fruit record from the list of fruits based on the type number and variety.
    """
    try:
        fruit_list = fruit_class_load(fruit_file)
    except ValueError:
        fruit_list = []

    fruit_len_prev = len(fruit_list)
    print(len(fruit_list))
    for i in range(0, len(fruit_list)):
        fruit = fruit_list[i]
        if fruit.get_type_num() == fruit_type_num and fruit.variety == variety:
            del fruit_list[i]
            break
    if fruit_len_prev == len(fruit_list):
        print("Fail to remove fruit, this fruit is not exist")
    fruit_information_store(fruit_list, fruit_file)










































