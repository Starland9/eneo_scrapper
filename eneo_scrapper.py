from datetime import datetime
from xmlrpc.client import DateTime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

class Localite:
    def __init__(self, quater: str, city: str, observations: str, start_date: str, end_date: str):
        self.quater = quater
        self.city = city
        self.observations = observations
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d %HH%M")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d %HH%M")


class EneoScraper:
    def __init__(self, driver: webdriver):
        self.eneo_url="https://alert.eneo.cm/"
        self.driver = driver
        self.driver.get(self.eneo_url)

    def get_regions(self) -> list[str]:
        regions_select = self.driver.find_element(By.ID, "regions")
        regions_options = regions_select.find_elements(By.TAG_NAME, "option")
        zones = [option.text for option in regions_options]
        return zones

    def search_locality(self, locality, region: str = None) -> list[Localite]:
        if region:
            regions_select = self.driver.find_element(By.ID, "regions")
            regions_options = regions_select.find_elements(By.TAG_NAME, "option")
            for option in regions_options:
                if option.text == region:
                    option.click()
                    break


        search_input = self.driver.find_element(By.ID, "localite")
        search_input.send_keys(locality)
        submit_button = self.driver.find_element(By.ID, "submitSaerch")
        submit_button.click()
        time.sleep(1)

        localite_container_div = self.driver.find_element(By.ID, "contentdata")

        localite_divs = localite_container_div.find_elements(By.CLASS_NAME, "outage")

        localites = []
        for localite_div in localite_divs:
            quater = localite_div.find_element(By.CLASS_NAME, "quartier").text
            city = localite_div.find_element(By.CLASS_NAME, "ville").text
            observations = localite_div.find_element(By.CLASS_NAME, "observations").text

            prog_date_div = localite_div.find_element(By.CLASS_NAME, "prog_date")

            date_split = prog_date_div.text.split(" ")
            date = prog_date_div.text.split(" ")[1]
            time_split = date_split[-1].split("-")
            start_date = f"{date} {time_split[0]}"
            end_date = f"{date} {time_split[1]}"

            localites.append(Localite(quater, city, observations, start_date, end_date))

        return localites
