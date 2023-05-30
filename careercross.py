from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import translate

translator = translate.Translator(to_lang="en", from_lang="ja")

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

chrome_options = Options()
# Run in headless mode without opening a browser window
chrome_options.add_argument("--headless")
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(
    options=chrome_options, executable_path=r"C:\Users\MY-PC\Downloads\Compressed\chromedriver.exe")

salary_regex = r"[\d-]+"

titles = ["70718445", "72998214", "73047701"]
skill_keywords = ["skills", "knowledge", "abilities",
                  "experience", "ability", "proficient"]
edu_degrees = ["Bachelor", "B.S.", "degree", "Master"]

job_names = []
job_urls = []
job_salaries = []
degrees = []
skills = []
num_of_exp = []

max_page = 5

for title in titles:
    for i in range(max_page + 1):
        url = f"https://www.careercross.com/en/job-search/result/{title}?page={i+1}"
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        job_tags = soup.find_all(
            "a", {"class": "job-details-url"})
        for tag in job_tags:
            job_names.append(tag["title"])
            job_urls.append(tag["href"])

for url in tqdm(job_urls):
    temp_skills = []
    driver.get(url)
    time.sleep(.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    salary_elements = soup.find_all(
        "span", {"id": "jsonld-base-salary"})
    for element in salary_elements:
        if element["data-salary-min"] == '' and element["data-salary-max"] == '':
            job_salaries.append(element.contents[0])
        elif element["data-salary-min"] == '':
            job_salaries.append(
                round(int(element["data-salary-max"])*0.0071, 1))
        elif element["data-salary-max"] == '':
            job_salaries.append(
                round(int(element["data-salary-min"])*0.0071, 1))
        else:
            job_salaries.append(
                round(((int(element["data-salary-min"]) + int(element["data-salary-max"]))/2*0.0071), 1))

    exp_elements = soup.find_all(
        "span", {"id": "jsonld-experience-requirements"})
    num_of_exp.append(exp_elements[0].contents[0])
    # print(exp_elements[0].contents[0])

    edu_elements = soup.find_all(
        "span", {"id": "jsonld-education-requirements"})
    for element in edu_elements:
        degrees.append(element.contents[0])

    skill_elements = soup.find_all(
        "span", {"id": "qualifications-required-skills"})
    try:
        li_elements = skill_elements[0].ul.find_all("li")
        for element in li_elements:
            if (skill_keywords[0].lower() in translator.translate(str(element.contents[0])).lower()) or (skill_keywords[1].lower() in translator.translate(str(element.contents[0])).lower()) or (skill_keywords[2].lower() in translator.translate(str(element.contents[0])).lower()) or (skill_keywords[3].lower() in translator.translate(str(element.contents[0])).lower()) or (skill_keywords[4].lower() in translator.translate(str(element.contents[0])).lower()):
                temp_skills.append(translator.translate(
                    str(element.contents[0])))
            else:
                pass
    except AttributeError:
        pass
    except IndexError:
        pass

    if len(temp_skills) != 0:
        skills.append(temp_skills)
    else:
        skills.append("None")

job_salaries = ["$" + str(x) if x != "None" else str(x) for x in job_salaries]
# print(len(degrees))
# print(len(num_of_exp))

df = pd.DataFrame(
    {'Job Title': job_names, 'Salary': job_salaries, 'Skills': skills, 'Education': degrees, 'Experience': num_of_exp, 'Job URL': job_urls})

df.to_excel("jpn.xlsx", sheet_name="JPN")
