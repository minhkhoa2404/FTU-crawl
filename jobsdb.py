from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
# Run in headless mode without opening a browser window
chrome_options.add_argument("--headless")
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(
    options=chrome_options, executable_path=r"chromedriver.exe")

salary_regex = r"[\d-]+"

titles = ["logistics", "warehouse", "demand planning"]
skill_keywords = ["skills", "knowledge", "abilities",
                  "experience", "ability", "proficient"]
edu_degrees = ["Bachelor", "B.S.", "degree", "Master"]

job_names = []
job_urls = []
job_salaries = []
degrees = []
skills = []
num_of_exp = []

max_page = 2

for title in titles:
    for i in range(max_page + 1):
        url = f"https://hk.jobsdb.com/hk/search-jobs/{title}/{i+1}"
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        job_tags = soup.find_all(
            "h1", {"class": "z1s6m00 _1hbhsw64y y44q7i0 y44q7i3 y44q7i21 y44q7ii"})
        for tag in job_tags:
            job_names.append(tag.a.div.span.contents[0])
            job_urls.append("https://hk.jobsdb.com" +
                            str(tag.a["href"]))

for url in tqdm(job_urls):
    temp_skills = []
    temp_degree = []
    temp_exp = []
    temp_salary = ""
    deg = ""
    num_exp = ""

    driver.get(url)
    time.sleep(.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    salary_elements = soup.find_all(
        "span", {"class": "z1s6m00 _1hbhsw64y y44q7i0 y44q7i1 y44q7i21 y44q7ii"})
    for salary_element in salary_elements:
        if "HK$" in salary_element.contents[0]:
            temp_salary = re.findall(
                salary_regex, str(salary_element.contents[0]).replace(",", ""))
            break
        else:
            temp_salary = "None"
    # print(temp_salary)
    additional_elements = soup.find_all(
        "div", {"class": "z1s6m00 _1hbhsw65a _1hbhsw6gi _5135ge2f"})
    try:
        if additional_elements[0].find_all(
                "div", {"class": "z1s6m00 _1hbhsw6r pmwfa50 pmwfa57"})[1].div.div.find_all("div", {"class": "z1s6m00 _1hbhsw66q"})[0].span.contents[0] == "Qualification":
            degrees.append(additional_elements[0].find_all(
                "div", {"class": "z1s6m00 _1hbhsw6r pmwfa50 pmwfa57"})[1].div.div.find_all("div", {"class": "z1s6m00 _1hbhsw66q"})[1].span.contents[0])
        else:
            degrees.append("None")
    except IndexError:
        degrees.append("None")

    try:
        if additional_elements[0].find_all(
                "div", {"class": "z1s6m00 _1hbhsw6r pmwfa50 pmwfa57"})[2].div.div.find_all("div", {"class": "z1s6m00 _1hbhsw66q"})[0].span.contents[0] == "Years of Experience":
            num_of_exp.append(additional_elements[0].find_all(
                "div", {"class": "z1s6m00 _1hbhsw6r pmwfa50 pmwfa57"})[2].div.div.find_all("div", {"class": "z1s6m00 _1hbhsw66q"})[1].span.contents[0])
        else:
            num_of_exp.append("None")
    except IndexError:
        num_of_exp.append("None")

    try:
        skill_elements_temp = soup.find(
            "div", {"data-automation": "jobDescription"})
        skill_elements = skill_elements_temp.span.div.find_all("ul")
    except AttributeError:
        pass

    for skill_element2 in skill_elements:
        for skill_element in skill_element2.find_all("li"):
            try:
                if (skill_keywords[0].lower() in skill_element.contents[0].lower()) or (skill_keywords[1].lower() in skill_element.contents[0].lower()) or (skill_keywords[2].lower() in skill_element.contents[0].lower()) or (skill_keywords[3].lower() in skill_element.contents[0].lower()) or (skill_keywords[4].lower() in skill_element.contents[0].lower()):
                    temp_skills.append(skill_element.contents[0])
                else:
                    pass
            except TypeError:
                pass
            except AttributeError:
                pass
    if len(temp_skills) != 0:
        skills.append(temp_skills)
    else:
        skills.append("None")
    job_salaries.append(temp_salary)

for i, salary in enumerate(job_salaries):
    if salary != "None":
        job_salaries.insert(
            i, round(((int(salary[0]) + int(salary[-1]))/2*0.127655), 1))
        job_salaries.remove(salary)

job_salaries = ["$" + str(x) if x != "None" else str(x) for x in job_salaries]

print(len(job_salaries))
print(len(job_names))
print(len(skills))
print(len(degrees))
print(len(num_of_exp))
print(len(job_urls))

df = pd.DataFrame(
    {'Job Title': job_names, 'Salary': job_salaries, 'Skills': skills, 'Education': degrees, 'Experience': num_of_exp, 'Job URL': job_urls})

df.to_excel("hk.xlsx", sheet_name="SGN")
