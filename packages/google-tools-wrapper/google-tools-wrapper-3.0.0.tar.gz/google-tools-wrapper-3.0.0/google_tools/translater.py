from sys import stdout
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup as bs

def translater(source_language: str, target_language: str, text: str) -> str:
    text = text.replace(' ', '%20') # making the text appropriate for the URL
        
    url_ = f'https://translate.google.com/?sl={source_language}&tl={target_language}&text={text}&op=translate' # base url

    try:
        Options = webdriver.ChromeOptions() # custom options
        Options.add_argument("--headless=new") # more efficiency & dont open chrome on user computer

        driver = webdriver.Chrome(options=Options) # generates an chrome page "emulator"

        # delete devtools message (selenium popup) | not working if user compile it by python.exe program.py
        stdout.write("\033[F")
        stdout.write("\033[K")
        stdout.write("\033[F")

        driver.get(url_) # """requests""" the page (emulate the page on the driver)

        # wait til load the traduction element (html) 
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ryNqvb')))

        page_code = driver.page_source # get page code

        soup = bs(page_code, 'html.parser')
    except TimeoutException as tout:
        return f"Something went wrong! Error: {str(tout)}"

    translated_text = soup.find('span', attrs={'class': 'ryNqvb', 'jsname': 'W297wb'}).text # finding the translation

    return translated_text
