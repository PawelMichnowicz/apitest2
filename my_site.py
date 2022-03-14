from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse

from typing import Optional
from scrapy import Selector
import requests

from sel_data import shop_max, shop_TV
from sel_update import equip_update

app = FastAPI()

@app.get('/get', response_class=HTMLResponse) 
def get_name(brand: Optional[str] = 'SAMSUNG', typeproduct: Optional[str] = 'TV', view: Optional[str] = 'min'):  
    brand = brand.upper()

    if typeproduct=='Smartphone':
        df = shop_max(brand, view)
    elif typeproduct=='TV':
        df = shop_TV(brand, view)  # one function
    return df.to_html() #matchcase / json

@app.get('/update', response_class=HTMLResponse) 
def update():  
    status = False         # status try/exception
    status = equip_update()
    if status:
        return "Data updated"
    else:
        return "Something wrong"
        




