from dataclasses import dataclass
from inspect import FullArgSpec
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#"//table[@id="rwd-table-large"]/tbody/tr[2]/td[14]"
class CurrentFuelRates:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://www.iftach.org/taxmatrix4/Taxmatrix.php")
    def getRates(self):
        STATE_INDEX = 1
        SPECIAL_DIESEL_RATE_INDEX,BIODIESEL_RATE_INDEX = 4,14

        TABLE_ID = "rwd-table-large"
        SPECIAL_DIESEL = "special diesel"
        BIODIESEL = "biodiesel"
        fuel_data = {}

        row = 1
        while True:
            try:
                path_to_state = f'//table[@id="{TABLE_ID}"]/tbody/tr[{row}]/td[{STATE_INDEX}]'
                path_to_sdrate = f'//table[@id="{TABLE_ID}"]/tbody/tr[{row}]/td[{SPECIAL_DIESEL_RATE_INDEX}]'
                path_to_bdrate = f'//table[@id="{TABLE_ID}"]/tbody/tr[{row}]/td[{BIODIESEL_RATE_INDEX}]'

                state = self.driver.find_element(By.XPATH, path_to_state).get_attribute("textContent")
                special_diesel_rate = self.driver.find_element(By.XPATH, path_to_sdrate).get_attribute("textContent")
                biodiesel_rate = self.driver.find_element(By.XPATH, path_to_bdrate).get_attribute("textContent")
                row+=1

                fuel_data[state]= {}
                fuel_data[state][SPECIAL_DIESEL]=special_diesel_rate if special_diesel_rate else "NA"
                fuel_data[state][BIODIESEL]=biodiesel_rate if biodiesel_rate else "NA"

            except:
                self.driver.quit()
                return fuel_data
                    
obj = CurrentFuelRates()
print(obj.getRates())
