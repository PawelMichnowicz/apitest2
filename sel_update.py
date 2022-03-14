from sel_avans import avans
from sel_xkom import xkom
from sel_neo import neo
from sel_data import list_of_shops 


list_of_products = ['TV', 'Smartphone']
list_of_brands = ['xiaomi', 'samsung', 'apple']


def equip_update():
    for brand in list_of_brands:
        for product in list_of_products:
            avans(brand=brand, type_product=product)
            neo(brand=brand, type_product=product)
            xkom(brand=brand, type_product=product)
    return True

