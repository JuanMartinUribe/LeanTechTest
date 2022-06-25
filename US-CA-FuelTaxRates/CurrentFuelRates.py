from dataclasses import dataclass
from inspect import FullArgSpec
from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tabulate import tabulate
import smtplib,ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import smtplib
import imghdr
from email.message import EmailMessage

class CurrentFuelRates:
    def __init__(self) -> None: 
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get("https://www.iftach.org/taxmatrix4/Taxmatrix.php")
    def getRates(self):
        STATE_INDEX = 1
        SPECIAL_DIESEL_RATE_INDEX,BIODIESEL_RATE_INDEX = 4,14
        TABLE_ID = "rwd-table-large"

        fuel_data = [["STATE","SPECIAL DIESEL","BIODIESEL"]]
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

                fuel_data.append([state,special_diesel_rate,biodiesel_rate])
            except:
                self.driver.quit()
                return fuel_data

def excelEmail(message,filename):

    EMAIL_ADDRESS = 'juanmartin104@gmail.com'
    EMAIL_PASSWORD = 'glymhdztujnmjwyl'


    msg = EmailMessage()
    msg['Subject'] = 'subject'

    msg['From'] = EMAIL_ADDRESS
    msg['To'] = "juanmartin104@gmail.com"


    msg.set_content('This is a plain text email')
    msg.add_alternative("""\
    <!DOCTYPE html>    
    <html>
    <head>
    <style>
    .r{
    text-align: left;
    }
    </style>
    </head>
    <body>
    <p>&nbsp;</p>
    <p><font size="4" face="Acme"><b>"""+message+"""<font size="4" face="Acme"><b>
    </body>
    </html>
    """, subtype='html')


    no_loc_path = "C:/Users/Juan/Documents/LeanTechTest/US-CA-FuelTaxRates/currentFuelRates.py"
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(no_loc_path, "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename='+filename)
    msg.attach(part)


    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
obj = CurrentFuelRates()
msg = tabulate(obj.getRates(), tablefmt='html')
excelEmail(msg,"currentFuelRates.py")