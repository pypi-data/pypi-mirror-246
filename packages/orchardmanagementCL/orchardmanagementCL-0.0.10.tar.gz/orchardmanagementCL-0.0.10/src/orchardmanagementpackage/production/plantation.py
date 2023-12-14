import src.orchardmanagementpackage.production.fruit_info as fruit_info
import pandas as pd

"""
This module contains classes and functions related to fruit cultivation regions, including the Region class,
area calculations, region summary report, and data storage using DataFrames.
"""

class Region():
    """
    Represents a region with specific fruit cultivation information, including region ID, fruit type number,
    variety, area, and area type.

    Attributes:
    - regionId (int): The unique identifier for the region.
    - fruit_type_num (int): The type number of the fruit cultivated in the region.
    - variety (str): The variety of the fruit cultivated in the region.
    - area (float): The area of the region for fruit cultivation.
    - areaType (str): The type of the region, either "market" or "pick".
    """
    areaType_list = ["market", "pick"]

    def __init__(self, regionId, fruit_type_num, variety, area, areaType):
        """
        Initializes an instance of the Region class.
        """
        self.regionId = regionId
        self.fruit_type_num = fruit_type_num
        self.variety = variety
        self.area = area
        self.areaType = areaType

    # def __str__(self):
    #     """
    #     Returns a string representation of the region.
    #     """
    #     return f"{self.regionId}, {self.fruit_type_num}, {self.variety}, {self.area}, {self.areaType}"

    def get_area_type(self):
        """
        Returns the area type of the region.
        """
        return self.areaType

    def set_area_type(self, areaType):
        """
        Sets the area type of the region.
        """
        if areaType in Region.areaType_list:
            self.areaType = areaType
        else:
            print("Invalid area type")

    def get_area(self):
        """
        Returns the area of the region.
        """
        return self.area

    def get_fruit(self, fruit_list):
        """
        Retrieves the specific fruit instance for the region.
        """
        return fruit_info.get_fruit(self.fruit_type_num, self.variety, fruit_list)

    def region_display(self, fruit_list):
        """
        Displays information about the region and the cultivated fruit.
        """
        fruit = self.get_fruit(fruit_list)
        if isinstance(fruit, fruit_info.Apple):
            print(f"Region {self.regionId}: {self.variety} apple. Region Type: {self.areaType}. Area: {self.get_area()}")
        elif isinstance(fruit, fruit_info.Cherry):
            print(f"Region {self.regionId}: {self.variety} cherry. Region Type: {self.areaType}. Area: {self.get_area()}")
        else:
            print(f"Region {self.regionId}: {self.variety} peach. Region Type: {self.areaType}. Area: {self.get_area()}")


def get_region(region_index, region_list):
    """Retrieve a region from the list based on the region ID."""
    for region in region_list:
        if region.regionId == region_index:
            return region


def set_picking_region(plantingRegion):
    """Set the area type of the planting region to 'pick'."""
    plantingRegion.set_area_type("pick")
    return plantingRegion


def set_marketing_region(plantingRegion):
    """Set the area type of the planting region to 'market'."""
    plantingRegion.set_area_type("market")
    return plantingRegion


def area_amount_variety(plantation_list, fruit_type_num, fruit_variety):
    """Get the total planting area for a specific fruit type and variety."""
    area_pick_sum = 0
    area_market_sum = 0

    for region in plantation_list:
        f_type_num = region.fruit_type_num
        f_variety = region.variety

        if f_type_num == fruit_type_num and fruit_variety == f_variety:
            if region.get_area_type() == "market":
                area_market_sum += region.area
            else:
                area_pick_sum += region.area
    return area_pick_sum, area_market_sum


def fruit_index_list(plantation_list, fruit_type_num, fruit_variety):
    """Get lists of region IDs for a specific fruit type and variety based on area type."""
    fruit_index_pick = []
    fruit_index_market = []
    for region in plantation_list:
        if region.fruit_type_num == fruit_type_num and region.variety == fruit_variety:
            if region.get_area_type() == "market":
                fruit_index_market.append(region.regionId)
            else:
                fruit_index_pick.append(region.regionId)
    return fruit_index_pick, fruit_index_market

def region_summary(fruit_list, region_list):
    """
    Generate a summary DataFrame with picking and marketing area information for each fruit type and variety.

    Returns: DataFrame containing picking and marketing area information along with region indices.
    """
    area_dict_pick = {}
    area_dict_market = {}

    index_dict_pick = {}
    index_dict_market = {}

    for f in fruit_list:
        fruit_type_num = f.get_type_num()
        variety = f.variety
        display_name = variety+ " " + f.type

        picking_regions, marketing_regions = fruit_index_list(region_list, fruit_type_num, variety)
        picking_area, marketing_area = area_amount_variety(region_list, fruit_type_num, variety)

        area_dict_pick[display_name] = picking_area
        area_dict_market[display_name] = marketing_area

        # Fill lists to the same length
        max_len = max(len(picking_regions), len(marketing_regions))
        index_dict_pick[display_name] = picking_regions + [None] * (max_len - len(picking_regions))
        index_dict_market[display_name] = marketing_regions + [None] * (max_len - len(marketing_regions))

    index_dict_pick = {key: str(value) for key, value in index_dict_pick.items()}
    index_dict_market = {key: str(value) for key, value in index_dict_market.items()}

    # Create summary dataframes
    df_area_pick = pd.DataFrame(area_dict_pick, index=["pick_area"])
    #df_area_market = pd.DataFrame(area_dict_market, index=["market_area"])
    df_area_market = pd.DataFrame(area_dict_market, index=["market_area"])

    df_index_pick = pd.DataFrame(index_dict_pick, index = ["picking_regions_index"])
    df_index_market = pd.DataFrame(index_dict_market, index = ["marketing_regions_index"])

    df_combined = pd.concat([df_area_pick, df_index_pick, df_area_market, df_index_market], axis=0)
    return df_combined


def area_summary(fruit_list,region_list):
    """
    Generate a summary DataFrame with picking and marketing area information for each fruit type. This summary will be
    used for inventory management

    Returns: DataFrame containing picking and marketing area information.
    """
    df_combined = region_summary(fruit_list,region_list)
    df_area_combined = pd.concat([df_combined.loc["pick_area"], df_combined.loc["market_area"]], axis=1)
    df_area_combined = df_area_combined.rename(columns={"pick_area": "picking_area", "market_area": "marketing_area"})

    index_mapping = {"apple": "1", "cherry": "2", "peach": "3"}
    df_area_combined.index = df_area_combined.index.map(
        lambda x: f"{index_mapping.get(x.split()[1], x.split()[1])} {x.split()[0]}")

    return df_area_combined


def region_saving(plantation_file,region_list):
    """
    Save region information from a list of Region instances to a DataFrame and store it in a CSV file.
    CSV file columns: 'regionId', 'fruit_type_num', 'variety', 'area', 'areaType'.
    """
    data_region = region_loading(plantation_file)

    region_info_list = []
    for r in region_list:
        regionId = r.regionId
        fruit_type_num = r.fruit_type_num
        variety = r.variety
        area = r.area
        areaType = r.get_area_type()

        region_info = [regionId, fruit_type_num, variety, area, areaType]
        region_info_list.append(region_info)

    data_region = pd.DataFrame(region_info_list, columns=data_region.columns)
    data_region.to_csv(plantation_file, index=False, header=True)
    #print("successful save")


def region_loading(plantation_file):
    """
    Load region information from a CSV file and convert it into a DataFrame.
    """
    try:
        data_region = pd.read_csv(plantation_file)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        title_list = ["regionId", "fruit_type_num", "variety", "area", "areaType"]
        data_region = pd.DataFrame(columns=title_list)
    return data_region


def region_class_tranfer(data_region):
    """
    Convert a DataFrame of region information into a list of Region class instances.
    """
    region_list = data_region.apply(
        lambda row: Region(row['regionId'], row['fruit_type_num'], row['variety'], row['area'],row['areaType']),
        axis=1).tolist()
    return region_list


class FruitNoneException(Exception):
    error_message = "planted fruit is not exist"
    def __init__(self, fruit):
        self.fruit = fruit

    def __str__(self):
        if self.fruit is None:
            return FruitNoneException.error_message

class RegionExistException(Exception):
    error_message = "input region is exist now"
    def __init__(self, regionId, regionId_set):
        self.regionId = regionId
        self.regionId_set = regionId_set

    def __str__(self):
        if self.regionId in self.regionId_set:
            return RegionExistException.error_message


def add_region(regionId, fruit_type_num, variety, area, areaType, fruit_list, planatation_file):
    """
    Add a new region to the list of regions.

    Note:
    add_region is used for plantation initialize, it will only call at the start of main.
    """
    data_region = region_loading(planatation_file)
    region_list = region_class_tranfer(data_region)
    regionId_set = set()
    for region in region_list:
        regionId_set.add(region.regionId)
    fruit = fruit_info.get_fruit(fruit_type_num, variety, fruit_list)
    if regionId in regionId_set:
        raise RegionExistException(regionId, regionId_set)
    elif fruit is None:
        raise FruitNoneException(fruit)
    else:
        region = Region(regionId, fruit_type_num, variety, area, areaType)
        region_list.append(region)
        region_saving(planatation_file, region_list)

    #
    # try:
    #     fruit = fruit_info.get_fruit(fruit_type_num, variety, fruit_list)
    #     if fruit is None:
    #         raise FruitNoneException(fruit)
    #     if regionId in regionId_set:
    #         raise RegionExistException(regionId, regionId_set)
    # except FruitNoneException as e:
    #     print(f"Fail to add region, {e}")
    # except RegionExistException as r:
    #     print(f"Fail to add region, {r}")





























