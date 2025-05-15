from typing import Union

from fastapi import FastAPI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from eneo_scrapper import EneoScraper

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

scrapper = EneoScraper(driver)
app = FastAPI()


@app.get("/regions")
async def get_regions():
    return {
        "regions": scrapper.get_regions()[1:]
    }

@app.get("/locality/{locality}/")
async def get_locality(locality: str, region: Union[str, None] = None):
    return {
        "localities": scrapper.search_locality(locality, region)
    }