from bs4 import BeautifulSoup
import requests
import re
from tqdm import tqdm
import pandas as pd

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

regex_pattern = r"[\d]+"
reg_exp = r"\b\d+-\d+\s*(?:year|years)?\b"
titles = ["logistics", "warehouse", "demand planning"]
skill_keywords = ["skills", "knowledge", "abilities", "experience", "ability"]
edu_degrees = ["Bachelor", "B.S.", "degree", "Master"]

job_names = []
job_urls = []
job_salaries = []
degrees = []
skills = []
num_of_exp = []

i = 0

for title in titles:
    flag = True
    while flag:
        url = f"https://www.michaelpage.com/jobs/{title}?sort_by=most_recent&page={i}"
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.text, 'html.parser')
        if soup.find("div", {"class": "view-empty"}) is None:
            job_tags = soup.find_all("div", {"class": "job-title"})
            for tag in job_tags:
                job_names.append(tag.h3.a.contents[0])
                job_urls.append(
                    "https://www.michaelpage.com" + tag.h3.a["href"])
            i += 1
        else:
            i = 0
            flag = False
            pass

for url in tqdm(job_urls):
    temp_skills = []
    temp_degree = []
    temp_exp = []
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.text, 'html.parser')
    salary = soup.find("span", {"class": "job-salary"})
    job_salaries.append(re.findall(
        regex_pattern, salary.text.replace(",", "")))
    try:
        applicant = soup.find("div", {"class": "successful-application"})
        success = applicant.div.ul.find_all("li")
    except AttributeError:
        applicant = soup.find("div", {"class": "successful-application"})
        success = applicant.div.find_all("p")
    for s in success:
        try:
            if (skill_keywords[0].lower() in s.contents[0].lower()) or (skill_keywords[1].lower() in s.contents[0].lower()) or (skill_keywords[2].lower() in s.contents[0].lower()) or (skill_keywords[3].lower() in s.contents[0].lower()) or (skill_keywords[4].lower() in s.contents[0].lower()):
                temp_skills.append(s.contents[0])
            else:
                pass
        except TypeError:
            pass
        try:
            if (edu_degrees[0].lower() in s.contents[0].lower()) or (edu_degrees[1].lower() in s.contents[0].lower()) or (edu_degrees[2].lower() in s.contents[0].lower()) or (edu_degrees[3].lower() in s.contents[0].lower()):
                temp_degree.append(s.contents[0])
            else:
                pass
        except TypeError:
            pass
        try:
            if len(re.findall(reg_exp, s.contents[0])) != 0:
                if re.findall(reg_exp, s.contents[0])[0] in s.contents[0]:
                    temp_exp.append(s.contents[0])
            else:
                pass
        except TypeError:
            pass

    if len(temp_skills) != 0:
        skills.append(temp_skills)
    else:
        skills.append("None")
    if len(temp_degree) != 0:
        degrees.extend(temp_degree)
    else:
        degrees.append("None")
    if len(temp_exp) != 0:
        num_of_exp.extend(temp_exp)
    else:
        num_of_exp.append("None")

job_salaries = [[int(s) for s in sublist] for sublist in job_salaries]
for i, salary in enumerate(job_salaries):
    job_salaries.insert(i, round(((salary[0] + salary[1])/2/12), 1))
    job_salaries.remove(salary)

job_salaries = ["$" + str(x) for x in job_salaries]

df = pd.DataFrame(
    {'Job Title': job_names, 'Salary': job_salaries, 'Skills': skills, 'Education': degrees, 'Experience': num_of_exp, 'Job URL': job_urls})

df.to_excel("test_data.xlsx")
