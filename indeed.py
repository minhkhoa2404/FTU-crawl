from tqdm import tqdm
import pandas as pd
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from undetected_chromedriver import ChromeOptions

"""
This file can be use to look for jobs from indeed.com in all regions (US, UK, Australia, China, Japan, Viet Nam,...) 
How we can bypass the Cloudflare captcha is to close the Chrome driver everytime we finish looking for the salaries, exp, degrees
"""


# Initiate undetected Chrome -> Bypass Cloudflare captcha
options = ChromeOptions()
options.add_argument('--lang=en')
prefs = {
    "translate_whitelists": {"fr": "en"},
    "translate": {"enabled": "true"}
}
options.add_experimental_option("prefs", prefs)

driver = uc.Chrome(
    options=options, driver_executable_path=r"C:\Users\MY-PC\Downloads\Compressed\chromedriver.exe")

# Regular expression for salary. For example, $1000-$2000 a year -> Only return 1000-2000
salary_regex = r"[\d-]+"

# Title to start query
titles = ["logistics", "warehouse", "demand planning"]
# keywords to check for skill
skill_keywords = ["skills", "knowledge", "abilities",
                  "experience", "ability", "proficient"]
# Keywords for education
edu_degrees = ["Bachelor", "B.S.", "degree", "Master"]

job_names = []
job_urls = []
job_salaries = []
degrees = []
skills = []
num_of_exp = []

# Number of page index to query, number of jobs depends on this
max_page = 3

# Start looking for job titles and job URLs
for title in titles:
    for i in range(max_page + 1):
        url = f"https://au.indeed.com/jobs?q={title}&start={i+1}0&"
        driver.get(url)
        tags = driver.find_elements(
            By.CLASS_NAME, "jcs-JobTitle")
        for tag in tags:
            job_names.append(tag.text)
            job_urls.append(tag.get_attribute("href"))

driver.close()

# After having the job URLs, start looking for skills, degrees and salary in each URL
for url in tqdm(job_urls):
    temp_skills = []
    temp_exp = []
    temp_edu = []
    temp_salaries = []
    driver = uc.Chrome()
    driver.get(url)
    job_descriptions = driver.find_elements(
        By.CLASS_NAME, "jobsearch-jobDescriptionText")
    salaries = driver.find_elements(
        By.CLASS_NAME, "jobsearch-JobMetadataHeader-item")
    for salary in salaries:
        temp_salaries.append(salary.text)
    print(temp_salaries)
    if len(temp_salaries) != 0:
        job_salaries.append(temp_salaries)
    else:
        job_salaries.append("None")
    for job_desc in job_descriptions:
        print(job_desc.text.split("\n"))
        for job in job_desc.text.split("\n"):
            # Check for if the text have keywords for experience in it
            if ("years" in job.lower() or "experience" in job.lower() or "minimum" in job.lower() or "at least" in job.lower()):
                temp_exp.append(job)
            # Skill keywords
            if (skill_keywords[0] in job.lower() or skill_keywords[1] in job.lower() or skill_keywords[2] in job.lower() or skill_keywords[3] in job.lower() or skill_keywords[4] in job.lower() or skill_keywords[5] in job.lower()) and job not in temp_exp:
                temp_skills.append(job)
            # Degrees checking
            if edu_degrees[0] in job.lower() or edu_degrees[1] in job.lower() or edu_degrees[2] in job.lower() or edu_degrees[3] in job.lower():
                temp_edu.append(job)
        if len(temp_skills) != 0:
            skills.append(temp_skills)
        else:
            skills.append("None")
        if len(temp_exp) != 0:
            num_of_exp.append(temp_exp)
        else:
            num_of_exp.append("None")
        if len(temp_edu) != 0:
            degrees.append(temp_edu)
        else:
            degrees.append("None")

    driver.close()

df = pd.DataFrame(
    {'Job Title': job_names, 'Salary': job_salaries, 'Skills': skills, 'Education': degrees, 'Experience': num_of_exp, 'Job URL': job_urls})

df.to_excel("au.xlsx", sheet_name="AU")
