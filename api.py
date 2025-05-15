from typing import Union, Optional
from fastapi import FastAPI

from eneo_scrapper import EneoScraper

scrapper = EneoScraper()
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