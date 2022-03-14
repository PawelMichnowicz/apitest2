from fastapi import FastAPI, Path
from fastapi.responses import HTMLResponse

from typing import Optional
from scrapy import Selector
import requests

from sel_data import shop_max

app = FastAPI()


@app.get('/get', response_class=HTMLResponse) 
def get_name(brand: Optional[str] = 'SAMSUNG'):  
    brand = brand.upper()
    df = shop_max(brand)
    return df.to_html()




