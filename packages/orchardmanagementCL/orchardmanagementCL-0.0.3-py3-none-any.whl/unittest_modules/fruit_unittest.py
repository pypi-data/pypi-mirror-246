import os.path
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import src.orchardmanagementpackage.production.fruit_info as fruit_info


class FruitTestCase(unittest.TestCase):

    def setUp(self):
        self.a1 = fruit_info.Apple("Ambrosia", "big", "very sweet", "less sour", "crunchy", 1.2, "pie")
        self.c1 = fruit_info.Cherry("Lapins", "small", "median sweet", "median sour", "soft", 2.99, "cans")
        self.p1 = fruit_info.Peach("Elberta", "big", "very sweet", "less sour", "crunchy", 1.2, "pie")
        self.p2 = fruit_info.Peach("Redhaven", "median", "median sweet", "less sour", "crunchy", 3.2, "pie, can")
        self.fruit_list = [self.a1,self.p1,self.c1, self.p2]

    def tearDown(self):
        del self.a1
        del self.c1
        del self.p1
        del self.p2
        del self.fruit_list

    def test_describe(self):
        self.a1_describe = "big, less sour, very sweet, crunchy.It is good for pie"
        self.c1_describe = "small, median sour, median sweet, soft.It is good for cans"
        self.p1_describe = "big, less sour, very sweet, crunchy.It is good for pie"
        self.p2_describe = "median, less sour, median sweet, crunchy.It is good for pie, can"

        self.assertEqual(self.a1.describe(), self.a1_describe)
        self.assertEqual(self.c1.describe(), self.c1_describe)
        self.assertEqual(self.p1.describe(), self.p1_describe)
        self.assertEqual(self.p2.describe(), self.p2_describe)

    def test_price_get(self):
        self.assertEqual(self.a1.get_price(), 1.2)
        self.assertEqual(self.c1.get_price(), 2.99)
        self.assertEqual(self.p1.get_price(), 1.2)
        self.assertEqual(self.p2.get_price(), 3.2)

    def test_price_set(self):
        self.a1.set_price(1.9)
        self.c1.set_price(1.6)
        self.p1.set_price(2.1)
        self.p2.set_price(3.5)

        self.assertEqual(self.a1.get_price(), 1.9)
        self.assertEqual(self.c1.get_price(), 1.6)
        self.assertEqual(self.p1.get_price(), 2.1)
        self.assertEqual(self.p2.get_price(), 3.5)

    def test_get_type_num(self):
        self.assertEqual(self.a1.get_type_num(), 1)
        self.assertEqual(self.c1.get_type_num(), 2)
        self.assertEqual(self.p1.get_type_num(), 3)
        self.assertEqual(self.p1.get_type_num(), 3)

    def test_get_available_season(self):
        self.assertTrue(self.a1.get_available_season(9))
        self.assertFalse(self.c1.get_available_season(9))
        self.assertTrue(self.p1.get_available_season(9))
        self.assertFalse(self.p2.get_available_season(9))


class FruitInfoTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a1 = fruit_info.Apple("Ambrosia", "big", "very sweet", "less sour", "crunchy", 1.2, "pie")
        cls.c1 = fruit_info.Cherry("Lapins", "small", "median sweet", "median sour", "soft", 2.99, "cans")
        cls.p1 = fruit_info.Peach("Elberta", "big", "very sweet", "less sour", "crunchy", 1.2, "pie")
        cls.p2 = fruit_info.Peach("Redhaven", "median", "median sweet", "less sour", "crunchy", 3.2, "pie, can")
        cls.fruit_list = [cls.a1,cls.p1,cls.c1,cls.p2]

    @classmethod
    def tearDownClass(cls):
        del cls.a1
        del cls.c1
        del cls.p1
        del cls.p2
        del cls.fruit_list
        print("Finish FruitInfoTestCase")

    def test_datetime_transfer(self):
        self.assertEqual(fruit_info.datetime_transfer("09-21"), 9)
        self.assertEqual(fruit_info.datetime_transfer("09-04"), 9)
        self.assertEqual(fruit_info.datetime_transfer("12-21"), 12)
        self.assertEqual(fruit_info.datetime_transfer("9-21"), 9)

    def test_fruit_available_check(self):
        self.assertTrue(fruit_info.fruit_available_check("09-21", self.a1))
        self.assertFalse(fruit_info.fruit_available_check("09-21", self.c1))
        self.assertFalse(fruit_info.fruit_available_check("12-21", self.p1))
        self.assertTrue(fruit_info.fruit_available_check("08-21", self.p2))


    def test_get_fruit(self):
        self.assertEqual(fruit_info.get_fruit(1, "Ambrosia", self.fruit_list), self.a1)
        self.assertEqual(fruit_info.get_fruit(2, "Lapins", self.fruit_list), self.c1)
        self.assertEqual(fruit_info.get_fruit(3, "Elberta", self.fruit_list), self.p1)
        self.assertEqual(fruit_info.get_fruit(3, "Redhaven", self.fruit_list), self.p2)

    def test_file_load(self):
        # test non exist file
        self.assertIsNone(fruit_info.file_load("../production_file_test/test_non_exist.csv"))
        # test empty file
        self.assertEqual(fruit_info.file_load("production_file_test/test_empty.csv"), [])
        # test file with one line file
        self.assertEqual(fruit_info.file_load("production_file_test/test_one.csv"),
                         [['1', 'Ambrosia', 'big', 'very sweet', 'less sour', 'crunchy', '1.2', 'pie']])
        # test file with multiple line
        self.assertEqual(fruit_info.file_load("production_file_test/test_mutiple.csv"),
                         [['1', 'Ambrosia', 'big', 'very sweet', 'less sour', 'crunchy', '1.2', 'pie'],
                          ['3', 'Elberta', 'big', 'very sweet', 'less sour', 'crunchy', '1.2', 'pie'],
                          ['2','Lapins','small','median sweet','median sour','soft','2.99', 'cans']])

    def test_fruit_class_load(self):
        # test non-exist file
        self.assertIsNone(fruit_info.fruit_class_load("../production_file_test/test_non_exist.csv"))
        # test empty file
        self.assertEqual(fruit_info.fruit_class_load("production_file_test/test_empty.csv"), [])
        # test one-line file
        load_a1 = fruit_info.fruit_class_load("production_file_test/test_one.csv")
        self.assertEqual(len(load_a1),1)
        self.assertEqual(load_a1[0].get_type_num(), self.a1.get_type_num())
        self.assertEqual(load_a1[0].describe(),self.a1.describe())
        # test multiple-line file
        load_fruit_list = fruit_info.fruit_class_load("production_file_test/test_mutiple.csv")
        self.assertEqual(len(load_fruit_list),3)
        for i in range(0,len(load_fruit_list)):
            self.assertEqual(load_fruit_list[i].get_type_num(), self.fruit_list[i].get_type_num())
            self.assertEqual(load_fruit_list[i].describe(), self.fruit_list[i].describe())

    def test_file_store(self):
        fruit_info.file_store("production_file_test/test_save.csv", [[1, 2, 3]])
        with open("production_file_test/test_save.csv", 'r') as file:
            content = file.read()
        self.assertIn("1,2,3",content)

        fruit_info.file_store("production_file_test/test_save.csv", [[1, 2, 3], [4, 5, 6]])
        with open("production_file_test/test_save.csv", 'r') as file:
            content = file.read()
        self.assertIn("1,2,3", content)
        self.assertIn("4,5,6",content)

        fruit_info.file_store("production_file_test/test_save.csv", [["abc", "bcd", "ace"]])
        with open("production_file_test/test_save.csv", 'r') as file:
            content = file.read()
        self.assertIn("abc,bcd,ace", content)

        fruit_info.file_store("production_file_test/test_save.csv", [["abc", 1, "bcd", 2, "ace"], ["efg", 1, "bcf", 2, "ace"]])
        with open("production_file_test/test_save.csv", 'r') as file:
            content = file.read()
        self.assertIn("abc,1,bcd,2,ace", content)
        self.assertIn("efg,1,bcf,2,ace", content)

    def test_fruit_information_store(self):
        csv_test_save = "production_file_test/test_save.csv"
        fruit_list_1 = [self.a1]
        fruit_list_2 = [self.a1, self.c1]
        fruit_list_3 = [self.p1, self.p2]
        fruit_list_4 = [self.a1, self.p1]

        fruit_info.fruit_information_store(fruit_list_1, csv_test_save)
        with open(csv_test_save, 'r') as file:
            content = file.read()
        self.assertIn("1,Ambrosia,big,very sweet,less sour,crunchy,1.2,pie", content)

        fruit_info.fruit_information_store(fruit_list_2, csv_test_save)
        with open(csv_test_save, 'r') as file:
            content = file.read()
        self.assertIn("1,Ambrosia,big,very sweet,less sour,crunchy,1.2,pie", content)
        self.assertIn("2,Lapins,small,median sweet,median sour,soft,2.99,cans", content)

        fruit_info.fruit_information_store(fruit_list_3, csv_test_save)
        with open(csv_test_save, 'r') as file:
            content = file.read()
        self.assertNotIn("1,Ambrosia,big,very sweet,less sour,crunchy,1.2,pie", content)
        self.assertIn("3,Elberta,big,very sweet,less sour,crunchy,1.2,pie", content)
        self.assertIn("3,Redhaven,median,median sweet,less sour,crunchy,3.2,\"pie, can\"", content)

        fruit_info.fruit_information_store(fruit_list_4, csv_test_save)
        with open(csv_test_save, 'r') as file:
            content = file.read()
        self.assertIn("1,Ambrosia,big,very sweet,less sour,crunchy,1.2,pie", content)
        self.assertIn("3,Elberta,big,very sweet,less sour,crunchy,1.2,pie", content)

class FruitInfoAddRemoveTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a1 = fruit_info.Apple("Ambrosia", "big", "very sweet", "less sour", "crunchy", 1.2, "pie")
        cls.c1 = fruit_info.Cherry("Lapins", "small", "median sweet", "median sour", "soft", 2.99, "cans")
        cls.p1 = fruit_info.Peach("Elberta", "big", "very sweet", "less sour", "crunchy", 1.2, "pie")
        cls.p2 = fruit_info.Peach("Redhaven", "median", "median sweet", "less sour", "crunchy", 3.2, "pie, can")
        cls.fruit_list = [cls.a1, cls.p1, cls.c1, cls.p2]
        cls.file_path = "production_file_test/test_fruit.csv"

        with open(cls.file_path, 'w', newline='') as csvfile:
            csvfile.truncate(0)

    @classmethod
    def tearDownClass(cls):
        del cls.a1
        del cls.c1
        del cls.p1
        del cls.p2
        del cls.fruit_list
        del cls.file_path
        print("Finish FruitInfoAddRemoveTestCase")

    def test_add_fruit(self):
        fruit_info.add_fruit(1, "Ambrosia", "big", "very sweet", "less sour", "crunchy", 1.2, "pie", self.file_path)
        load_fruit_list = fruit_info.fruit_class_load(self.file_path)
        self.assertEqual(load_fruit_list[0].get_type_num(), self.a1.get_type_num())
        self.assertEqual(load_fruit_list[0].describe(), self.a1.describe())

        fruit_info.add_fruit(1, "Ambrosia", "small", "very sweet", "less sour", "crunchy", 1.2, "pie", self.file_path)
        with open(self.file_path, 'r') as file:
            content = file.read()
        self.assertNotIn("1,Ambrosia,small,very sweet,less sour,crunchy,1.2,pie", content)

        fruit_info.add_fruit(3, "Elberta", "big", "very sweet", "less sour", "crunchy", 1.2, "pie", self.file_path)
        load_fruit_list = fruit_info.fruit_class_load(self.file_path)
        for i in range(0,len(load_fruit_list)):
            self.assertEqual(load_fruit_list[i].get_type_num(), self.fruit_list[i].get_type_num())
            self.assertEqual(load_fruit_list[i].describe(), self.fruit_list[i].describe())

        self.assertFalse(fruit_info.add_fruit(2, "abc", "small", "median sweet", "median sour", "soft", 2.99, "cans", self.file_path))
        load_fruit_list = fruit_info.fruit_class_load(self.file_path)
        for i in range(0, len(load_fruit_list)):
            self.assertEqual(load_fruit_list[i].get_type_num(), self.fruit_list[i].get_type_num())
            self.assertEqual(load_fruit_list[i].describe(), self.fruit_list[i].describe())


    def test_remove(self):
        with open(self.file_path, 'w', newline='') as csvfile:
            csvfile.truncate(0)

        fruit_info.add_fruit(1, "Ambrosia", "small", "very sweet", "less sour", "crunchy", 1.2, "pie", self.file_path)
        # test successfully remove
        fruit_info.remove_fruit(1, "Ambrosia", self.file_path)
        with open(self.file_path, 'r') as file:
            content = file.read()
        self.assertNotIn("1,Ambrosia,small,very sweet,less sour,crunchy,1.2,pie", content)

        fruit_info.add_fruit(1, "Ambrosia", "small", "very sweet", "less sour", "crunchy", 1.2, "pie", self.file_path)
        # test not able to remove with unpaired type_num and variety
        fruit_info.remove_fruit(2, "Ambrosia", self.file_path)
        with open(self.file_path, 'r') as file:
            content = file.read()
        self.assertIn("1,Ambrosia,small,very sweet,less sour,crunchy,1.2,pie", content)

        fruit_info.add_fruit(2, "Lapins", "small", "median sweet", "median sour", "soft", 2.99, "cans", self.file_path)
        # test not able to remove with wrong type_num and varitey
        fruit_info.remove_fruit(3, "ABC", self.file_path)
        with open(self.file_path, 'r') as file:
            content = file.read()
        self.assertIn("1,Ambrosia,small,very sweet,less sour,crunchy,1.2,pie", content)
        self.assertIn("2,Lapins,small,median sweet,median sour,soft,2.99,cans",content)

        fruit_info.remove_fruit(4, "Lapins", self.file_path)
        with open(self.file_path, 'r') as file:
            content = file.read()
        self.assertIn("1,Ambrosia,small,very sweet,less sour,crunchy,1.2,pie", content)
        self.assertIn("2,Lapins,small,median sweet,median sour,soft,2.99,cans", content)


if __name__ == '__main__':
    unittest.main()
