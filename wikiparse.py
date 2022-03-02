# Set-ExecutionPolicy Unrestricted -Scope Process
# ./.myven/Scripts/activate
# uvicorn wikiparse:app --reload

from fastapi import FastAPI, Path
from typing import Optional
from fastapi.responses import HTMLResponse

from scrapy import Selector
import requests

app = FastAPI()

# 'https://pl.wikipedia.org/wiki/Pies_domowy'
@app.get('/get-text', response_class=HTMLResponse) 
def get_name(url: Optional[str] = 'https://pl.wikipedia.org/wiki/Pies_domowy'):  
    html = requests.get(url).content
    sel = Selector(text = html)
    list_of_words = sel.xpath('//body//text()').extract()
    text = ' '.join(list_of_words)
    text = text.replace("\n", '<br>').replace('\t', '  ')
    return text


@app.get('/get-img', response_class=HTMLResponse) 
def get_name(url: Optional[str] = 'https://pl.wikipedia.org/wiki/Pies_domowy'):  
    html = requests.get(url).content
    sel = Selector(text = html)
    list_of_img = sel.xpath('//img').extract()
    images = '<br>'.join(list_of_img)
    return images


@app.get('/get-all', response_class=HTMLResponse) 
def get_name(url: Optional[str] = 'https://pl.wikipedia.org/wiki/Pies_domowy'):  
    html = requests.get(url).content
    sel = Selector(text = html)
    list_of_all = sel.xpath("//img | //body//text()").extract()
    all = ' '.join(list_of_all)
    return all

