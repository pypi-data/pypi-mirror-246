import src.orchardmanagementpackage.production.fruit_info as fruit_info
import src.orchardmanagementpackage.production.plantation as plantation
fruit_list = fruit_info.fruit_class_load("fruits_test.csv")
region_list = []
area = 10
## set up regions
for i in range(0,len(fruit_list)):
    fruit = fruit_list[i]
    fruit_type_num = fruit.get_type_num()
    fruit_variety = fruit.variety
    area += 10
    region = plantation.Region(i + 1, fruit_type_num, fruit_variety, area, areaType="market")
    if i >= 1:
        region = plantation.set_picking_region(region)
        if i == 1:
            region = plantation.set_marketing_region(region)
    region_list.append(region)
for i in region_list:
    print(i.get_area_type())




plantation_file = "plantations_test.csv"
plantation.region_saving(plantation_file, region_list)

df_region = plantation.region_loading(plantation_file)
print(df_region)

region_list = plantation.region_class_tranfer(df_region)
print(region_list)
for region in region_list:
    print(region)
    print(region.get_fruit(fruit_list))

r1, r2 = plantation.fruit_index_list(region_list, 1, "Ambrosia")
print(r1)
print(r2)

print(plantation.area_amount_variety(region_list, 1, "Ambrosia"))


df_summary = plantation.region_summary(fruit_list, region_list)
print(df_summary)

d = plantation.area_summary(fruit_list, region_list)
print(d)

for region in region_list:
    region.region_display(fruit_list)

region_searched = plantation.get_region(1, region_list)
print(region_searched)

# plantation.add_region(3, 2, "Lapins", 40, "pick",
#                       fruit_list, plantation_file)
# plantation.add_region(4, 2, "Lapins", 40, "pick",
#                       fruit_list, plantation_file)

print(region_list)
print(len(region_list))
print(plantation_file)
df_summary_2 = plantation.region_summary(fruit_list, region_list)
print(df_summary_2)
print(plantation.area_summary(fruit_list, region_list))

