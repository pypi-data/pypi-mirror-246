import os.path
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
import pandas as pd
import src.orchardmanagement_package.production.fruit_info as fruit_info
import src.orchardmanagement_package.production.plantation as plantation
from io import StringIO


class RegionTestCase(unittest.TestCase):

    def setUp(self):
        self.fruit_list = fruit_info.fruit_class_load("production_file_test/test_mutiple.csv")
        self.a1 = self.fruit_list[0]
        self.p1 = self.fruit_list[1]
        self.c1 = self.fruit_list[2]
        self.r1 = plantation.Region(1, 1, "Ambrosia", 20, "market")
        self.r2 = plantation.Region(2, 3, "Elberta", 30, "market")
        self.r3 = plantation.Region(3, 2, "Lapins", 40, "pick")
        self.r4 = plantation.Region(4, 2, "Lapins", 40, "pick")
        self.region_list = [self.r1, self.r2, self.r3, self.r4]

    def tearDown(self):
        del self.fruit_list
        del self.a1
        del self.p1
        del self.c1
        del self.r1
        del self.r2
        del self.r3
        del self.r4
        del self.region_list

    def test_get_area_type(self):
        self.assertEqual(self.r1.get_area_type(), "market")
        self.assertEqual(self.r2.get_area_type(), "market")
        self.assertEqual(self.r3.get_area_type(), "pick")
        self.assertEqual(self.r4.get_area_type(), "pick")

    def test_set_area_type(self):
        # test unchanged area_type
        self.r1.set_area_type("market")
        self.assertEqual(self.r1.get_area_type(), "market")
        self.r3.set_area_type("pick")
        self.assertEqual(self.r3.get_area_type(), "pick")

        # test changed area_type
        self.r2.set_area_type("pick")
        self.assertEqual(self.r2.get_area_type(), "pick")
        self.r4.set_area_type("market")
        self.assertEqual(self.r4.get_area_type(), "market")

    def test_get_area(self):
        self.assertEqual(self.r1.get_area(), 20)
        self.assertEqual(self.r2.get_area(), 30)
        self.assertEqual(self.r3.get_area(), 40)
        self.assertEqual(self.r4.get_area(), 40)

    def test_get_fruit(self):
        fruit1 = self.r1.get_fruit(self.fruit_list)
        fruit2 = self.r2.get_fruit(self.fruit_list)
        fruit3 = self.r3.get_fruit(self.fruit_list)
        fruit4 = self.r4.get_fruit(self.fruit_list)

        self.assertEqual(fruit1.get_type_num(),self.a1.get_type_num())
        self.assertEqual(fruit1.describe(), self.a1.describe())

        self.assertEqual(fruit2.get_type_num(), self.p1.get_type_num())
        self.assertEqual(fruit2.describe(), self.p1.describe())

        self.assertEqual(fruit3.get_type_num(), self.c1.get_type_num())
        self.assertEqual(fruit3.describe(), self.c1.describe())

        self.assertEqual(fruit4.get_type_num(), self.c1.get_type_num())
        self.assertEqual(fruit4.describe(), self.c1.describe())

    def test_region_display(self):
        # test print output
        original_stdout = sys.stdout
        sys.stdout = StringIO()
        self.r1.region_display(self.fruit_list)
        printed_output = sys.stdout.getvalue().strip()
        sys.stdout = original_stdout
        self.assertEqual(printed_output, "Region 1: Ambrosia apple. Region Type: market. Area: 20")

        original_stdout = sys.stdout
        sys.stdout = StringIO()
        self.r2.region_display(self.fruit_list)
        printed_output = sys.stdout.getvalue().strip()
        sys.stdout = original_stdout
        self.assertEqual(printed_output, "Region 2: Elberta peach. Region Type: market. Area: 30")

        original_stdout = sys.stdout
        sys.stdout = StringIO()
        self.r3.region_display(self.fruit_list)
        printed_output = sys.stdout.getvalue().strip()
        sys.stdout = original_stdout
        self.assertEqual(printed_output, "Region 3: Lapins cherry. Region Type: pick. Area: 40")

        original_stdout = sys.stdout
        sys.stdout = StringIO()
        self.r4.region_display(self.fruit_list)
        printed_output = sys.stdout.getvalue().strip()
        sys.stdout = original_stdout
        self.assertEqual(printed_output, "Region 4: Lapins cherry. Region Type: pick. Area: 40")

    def test_get_region(self):
        r1_get = plantation.get_region(1, self.region_list)
        r2_get = plantation.get_region(2, self.region_list)
        r3_get = plantation.get_region(3, self.region_list)
        r4_get = plantation.get_region(4, self.region_list)
        self.assertEqual(r1_get.regionId, self.r1.regionId)
        self.assertEqual(r1_get.fruit_type_num, self.r1.fruit_type_num)
        self.assertEqual(r1_get.variety, self.r1.variety)
        self.assertEqual(r1_get.get_area(), self.r1.get_area())
        self.assertEqual(r1_get.get_area_type(), self.r1.get_area_type())

        self.assertEqual(r2_get.regionId, self.r2.regionId)
        self.assertEqual(r2_get.fruit_type_num, self.r2.fruit_type_num)
        self.assertEqual(r2_get.variety, self.r2.variety)
        self.assertEqual(r2_get.get_area(), self.r2.get_area())
        self.assertEqual(r2_get.get_area_type(), self.r2.get_area_type())

        self.assertEqual(r3_get.regionId, self.r3.regionId)
        self.assertEqual(r3_get.fruit_type_num, self.r3.fruit_type_num)
        self.assertEqual(r3_get.variety, self.r3.variety)
        self.assertEqual(r3_get.get_area(), self.r3.get_area())
        self.assertEqual(r3_get.get_area_type(), self.r3.get_area_type())

        self.assertEqual(r4_get.regionId, self.r4.regionId)
        self.assertEqual(r4_get.fruit_type_num, self.r4.fruit_type_num)
        self.assertEqual(r4_get.variety, self.r4.variety)
        self.assertEqual(r4_get.get_area(), self.r4.get_area())
        self.assertEqual(r4_get.get_area_type(), self.r4.get_area_type())

    def test_set_picking_region(self):
        plantation.set_picking_region(self.r1)
        self.assertEqual(self.r1.get_area_type(), "pick")

        plantation.set_picking_region(self.r2)
        self.assertEqual(self.r2.get_area_type(), "pick")

        plantation.set_picking_region(self.r3)
        self.assertEqual(self.r3.get_area_type(), "pick")

        plantation.set_picking_region(self.r4)
        self.assertEqual(self.r4.get_area_type(), "pick")

    def test_set_marketing_region(self):
        plantation.set_marketing_region(self.r1)
        self.assertEqual(self.r1.get_area_type(), "market")

        plantation.set_marketing_region(self.r2)
        self.assertEqual(self.r2.get_area_type(), "market")

        plantation.set_marketing_region(self.r3)
        self.assertEqual(self.r3.get_area_type(), "market")

        plantation.set_marketing_region(self.r4)
        self.assertEqual(self.r4.get_area_type(), "market")

    def test_area_amount_variety(self):
        # test with valid fruit type_num and valid fruit variety
        area1, area2 = plantation.area_amount_variety(self.region_list, 1, "Ambrosia")
        self.assertEqual(area1, 0)
        self.assertEqual(area2, 20)

        # test with valid fruit type_num and invalid fruit variety
        area1, area2 = plantation.area_amount_variety(self.region_list, 1, "Lapin")
        self.assertEqual(area1, 0)
        self.assertEqual(area2, 0)

        # test with invalid fruit type_num and valid fruit variety
        area1, area2 = plantation.area_amount_variety(self.region_list, 6, "Lapin")
        self.assertEqual(area1, 0)
        self.assertEqual(area2, 0)

        # test with invalid fruit type_num and invalid fruit variety
        area1, area2 = plantation.area_amount_variety(self.region_list, 6, "abc")
        self.assertEqual(area1, 0)
        self.assertEqual(area2, 0)

    def test_region_summary(self):
        # test region summary with empty region_list
        region_list_1 = []
        region_list_2 = [self.r1, self.r2, self.r3]
        df1 = plantation.region_summary(self.fruit_list, region_list_1)
        self.assertEqual(df1["Lapins cherry"]["pick_area"],0)
        self.assertEqual(df1["Lapins cherry"]["market_area"], 0)
        self.assertEqual(df1["Elberta peach"]["pick_area"], 0)
        self.assertEqual(df1["Elberta peach"]["market_area"], 0)
        self.assertEqual(df1["Ambrosia apple"]["pick_area"], 0)
        self.assertEqual(df1["Ambrosia apple"]["market_area"], 0)

        self.assertEqual(df1["Lapins cherry"]["picking_regions_index"], '[]')
        self.assertEqual(df1["Lapins cherry"]["marketing_regions_index"], '[]')
        self.assertEqual(df1["Elberta peach"]["picking_regions_index"], '[]')
        self.assertEqual(df1["Elberta peach"]["marketing_regions_index"], '[]')
        self.assertEqual(df1["Ambrosia apple"]["picking_regions_index"], '[]')
        self.assertEqual(df1["Ambrosia apple"]["marketing_regions_index"], '[]')

        # test region summary with empty fruit_list
        fruit_list_1 = []
        df2 = plantation.region_summary(fruit_list_1, region_list_2)
        self.assertTrue(df2.empty)

        # test region summary with empty fruit_list and empty region_list
        df3 = plantation.region_summary(fruit_list_1, region_list_1)
        self.assertTrue(df3.empty)

        # test region summary with fruit_list and empty region_list
        df4 = plantation.region_summary(self.fruit_list, self.region_list)
        self.assertEqual(df4["Lapins cherry"]["pick_area"], 80)
        self.assertEqual(df4["Lapins cherry"]["market_area"], 0)
        self.assertEqual(df4["Elberta peach"]["pick_area"], 0)
        self.assertEqual(df4["Elberta peach"]["market_area"], 30)
        self.assertEqual(df4["Ambrosia apple"]["pick_area"], 0)
        self.assertEqual(df4["Ambrosia apple"]["market_area"], 20)

        self.assertEqual(df4["Lapins cherry"]["picking_regions_index"], '[3, 4]')
        self.assertEqual(df4["Lapins cherry"]["marketing_regions_index"], '[None, None]')
        self.assertEqual(df4["Elberta peach"]["picking_regions_index"], '[None]')
        self.assertEqual(df4["Elberta peach"]["marketing_regions_index"], '[2]')
        self.assertEqual(df4["Ambrosia apple"]["picking_regions_index"], '[None]')
        self.assertEqual(df4["Ambrosia apple"]["marketing_regions_index"], '[1]')

    def test_area_summary(self):
        df1 = plantation.area_summary(self.fruit_list, self.region_list)
        self.assertEqual(df1["picking_area"]["1 Ambrosia"], 0)
        self.assertEqual(df1["picking_area"]["3 Elberta"], 0)
        self.assertEqual(df1["picking_area"]["2 Lapins"], 80)
        self.assertEqual(df1["marketing_area"]["1 Ambrosia"], 20)
        self.assertEqual(df1["marketing_area"]["3 Elberta"], 30)
        self.assertEqual(df1["marketing_area"]["2 Lapins"], 0)

        fruit_list_1 = []
        region_list_1 = []

        df2 = plantation.area_summary(fruit_list_1, self.region_list)
        self.assertTrue(df2.empty)

        df3 = plantation.area_summary(fruit_list_1, region_list_1)
        self.assertTrue(df3.empty)

        df4 = plantation.area_summary(self.fruit_list, region_list_1)
        self.assertEqual(df4["picking_area"]["1 Ambrosia"], 0)
        self.assertEqual(df4["picking_area"]["3 Elberta"], 0)
        self.assertEqual(df4["picking_area"]["2 Lapins"], 0)
        self.assertEqual(df4["marketing_area"]["1 Ambrosia"], 0)
        self.assertEqual(df4["marketing_area"]["3 Elberta"], 0)
        self.assertEqual(df4["marketing_area"]["2 Lapins"], 0)

    def test_region_loading(self):
        # test not exist csv
        d0 = plantation.region_loading("../production_file_test/test_not_exist.csv")
        self.assertTrue(d0.empty)

        # test empty csv
        d1 = plantation.region_loading("production_file_test/test_empty.csv")
        self.assertTrue(d1.empty)

        # test one line csv
        d2 = plantation.region_loading("production_file_test/test_one_region.csv")
        data = {
            'regionId': [1],
            'fruit_type_num': [1],
            'variety': ['Ambrosia'],
            'area': [20],
            'areaType': ['market']
        }
        df = pd.DataFrame(data)
        self.assertTrue(df.equals(d2))

        # test multiple line csv
        d3 = plantation.region_loading("production_file_test/test_multiple_region.csv")
        data2 = {
            'regionId': [1, 2, 3, 4],
            'fruit_type_num': [1, 3, 2, 2],
            'variety': ['Ambrosia', 'Elberta', 'Lapins', 'Lapins'],
            'area': [20, 30, 40, 40],
            'areaType': ['market', 'market', 'pick', 'pick']
        }
        df2 = pd.DataFrame(data2)
        self.assertTrue(df2.equals(d3))

    def test_fruit_index_list(self):
        i1, i2 = plantation.fruit_index_list(self.region_list, 1, "Ambrosia")
        self.assertEqual(i1, [])
        self.assertEqual(i2, [1])

        i3, i4 = plantation.fruit_index_list(self.region_list, 1, "Lapins")
        self.assertEqual(i3, [])
        self.assertEqual(i4, [])

        i5, i6 = plantation.fruit_index_list(self.region_list, 2, "Lapins")
        self.assertEqual(i5, [3, 4])
        self.assertEqual(i6, [])

        i7, i8 = plantation.fruit_index_list(self.region_list, 3, "Elberta")
        self.assertEqual(i7, [])
        self.assertEqual(i8, [2])

    def test_region_class_transfer(self):
        # test valid region dataframe
        data = {
            'regionId': [1],
            'fruit_type_num': [1],
            'variety': ['Ambrosia'],
            'area': [20],
            'areaType': ['market']
        }
        df = pd.DataFrame(data)
        r_list_1 = plantation.region_class_tranfer(df)
        self.assertEqual(len(r_list_1),1)
        self.assertTrue(isinstance(r_list_1[0], plantation.Region))

        # test empty region dataframe
        data2 = {
            'regionId': [],
            'fruit_type_num': [],
            'variety': [],
            'area': [],
            'areaType': []
        }
        df2 = pd.DataFrame(data2)
        r_list_2 = plantation.region_class_tranfer(df2)
        self.assertEqual([], r_list_2)

        # test region dataframe(more than one region)
        data3 = {
            'regionId': [1, 2, 3, 4],
            'fruit_type_num': [1, 3, 2, 2],
            'variety': ['Ambrosia', 'Elberta', 'Lapins', 'Lapins'],
            'area': [20, 30, 40, 40],
            'areaType': ['market', 'market', 'pick', 'pick']
        }
        df3 = pd.DataFrame(data3)
        r_list_3 = plantation.region_class_tranfer(df3)
        self.assertEqual(4,len(r_list_3))
        for i in range(0,len(r_list_3)):
            self.assertTrue(isinstance(r_list_3[i], plantation.Region))

        # test empty dataframe(no list/index)
        data4 = {}
        df4 = pd.DataFrame(data4)
        with self.assertRaises(Exception) as context:
            result = plantation.region_class_tranfer(df4)
        self.assertIsInstance(context.exception, AttributeError)

    def test_region_saving(self):
        file1 = "production_file_test/test_region.csv"
        plantation.region_saving(file1, self.region_list)

        with open(file1, 'r') as file:
            content = file.read()
        self.assertIn("regionId,fruit_type_num,variety,area,areaType", content)
        self.assertIn("1,1,Ambrosia,20,market", content)
        self.assertIn("2,3,Elberta,30,market", content)
        self.assertIn("3,2,Lapins,40,pick", content)
        self.assertIn("4,2,Lapins,40,pick", content)

        plantation.region_saving(file1, [])
        with open(file1, 'r') as file:
            content = file.read()
        self.assertIn("regionId,fruit_type_num,variety,area,areaType", content)
        self.assertNotIn("1,1,Ambrosia,20,market", content)

        plantation.region_saving(file1, [self.region_list[1]])
        with open(file1, 'r') as file:
            content = file.read()
        self.assertIn("regionId,fruit_type_num,variety,area,areaType", content)
        self.assertIn("2,3,Elberta,30,market", content)

        plantation.region_saving(file1, [self.r1, self.r3])
        with open(file1, 'r') as file:
            content = file.read()
        self.assertIn("regionId,fruit_type_num,variety,area,areaType", content)
        self.assertIn("1,1,Ambrosia,20,market", content)
        self.assertIn("3,2,Lapins,40,pick", content)

    def test_add_region(self):
        file1 = "production_file_test/test_region.csv"

        #check if add region with unexist fruit
        with self.assertRaises(plantation.FruitNoneException):
            plantation.add_region(2, 2, "Ambrosia", 20, "market", self.fruit_list, file1)

        # check if add region with existed regionId
        with self.assertRaises(plantation.RegionExistException):
            plantation.add_region(3, 1, "Ambrosia", 20, "market", self.fruit_list, file1)

        plantation.add_region(4, 1, "Ambrosia", 40, "pick",
                              self.fruit_list, file1)
        with open(file1, 'r') as file:
            content = file.read()
        self.assertIn("4,1,Ambrosia,40,pick", content)

        plantation.add_region(5, 2, "Lapins", 40, "pick",
                              self.fruit_list, file1)
        with open(file1, 'r') as file:
            content = file.read()
        self.assertIn("5,2,Lapins,40,pick", content)

if __name__ == '__main__':
    unittest.main()
