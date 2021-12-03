import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pandas


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

s=Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s, options=chrome_options)
driver.maximize_window()

action = webdriver.common.action_chains.ActionChains(driver)

full_data = pandas.DataFrame({"Major": [],
            "Early Career Pay": [],
            "Mid-Career Pay": [],
            "Meaningfulness": []
            })

def scrape_page():
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    add_table(soup)

def next_page(soup):
    current_page = int(soup.select(".pagination__btn.pagination__btn--active")[0].text)
    driver.get(f"https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/{current_page+1}")
    time.sleep(1)
    scrape_page()

def add_table(soup):
    global full_data
    rows = soup.find_all(class_="data-table__row")
    if len(rows)>0:
        majors = []
        early_pay = []
        mid_pay = []
        meaningfulness = []
        for i in range(len(rows)):
            majors.append(soup.select(".data-table__cell.csr-col--school-name")[i].text.split(":")[1])
            early_pay.append(soup.select(".data-table__cell.csr-col--right")[i*3].text.split(":")[1])
            mid_pay.append(soup.select(".data-table__cell.csr-col--right")[i*3+1].text.split(":")[1])
            meaningfulness.append(soup.select(".data-table__cell.csr-col--right")[i*3+2].text.split(":")[1])
        data = {"Major": majors,
                "Early Career Pay": early_pay,
                "Mid-Career Pay": mid_pay,
                "Meaningfulness": meaningfulness
                }
        data = pandas.DataFrame.from_dict(data)
        data.to_csv('payscale_data.csv', mode='a', header=False, index=False)
        next_page(soup)

driver.get("https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors/page/1")

time.sleep(1)

scrape_page()

