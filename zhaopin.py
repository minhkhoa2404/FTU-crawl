from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import translate
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


"""
This file can be use to look for jobs from China but can only extract the job names, salaries and job URLs -> After having these things, we can crawl the skills, degrees and exp manually :))) 
"""

# Having a translator to translate the salary from Chinese to English
translator = translate.Translator(to_lang="en", from_lang="zh")

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

chrome_options = Options()
chrome_options.add_argument("start-maximized")
chrome_options.add_experimental_option(
    "excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument('--disable-blink-features=AutomationControlled')
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(
    options=chrome_options, executable_path=r"chromedriver.exe")

salary_regex = r"[\d-]+"

titles = ["logistics", "warehouse", "demand planning",
          "Transportation", "Supply Chain"]
skill_keywords = ["skills", "knowledge", "abilities",
                  "experience", "ability", "proficient"]
edu_degrees = ["Bachelor", "B.S.", "degree", "Master"]

job_names = []
job_urls = []
job_salaries = []
degrees = []
skills = []
num_of_exp = []

for title in titles:
    url = f"https://sou.zhaopin.com/?kw={title}"
    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "#positionList-hook > div > div:nth-child(1) > a")))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup)
    job_tags = soup.find_all(
        "a", {"class": "joblist-box__iteminfo iteminfo"})
    for tag in job_tags:
        if tag["href"] not in job_urls:
            job_urls.append(tag["href"])
            job_names.append(tag.find(
                "div", {"class": "iteminfo__line iteminfo__line1"}).div.span["title"])
            salary = tag.find(
                "div", {"class": "iteminfo__line iteminfo__line2"}).div.p.text
            job_salaries.append(salary)

job_salaries = [translator.translate(x) for x in tqdm(job_salaries)]
job_salaries = [re.findall(salary_regex, x.replace(",", ""))
                for x in job_salaries]
print(job_salaries)
print(f"{len(job_names)} - {len(job_salaries)} - {len(job_urls)}")

df = pd.DataFrame(
    {'Job Title': job_names, 'Salary': job_salaries, 'Job URL': job_urls})

df.to_excel("cn.xlsx", sheet_name="CN")
