# Brief description

## Cloudflare captcha
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/d59c9bb3-54ad-494c-936e-18eb8d66ca21)
- When crawling the data, some website might require user to do some verification to avoid traffic -> We need to find a way to bypass this when automatically crawl the website
## Using undetected Chrome
- Can be used to by pass the Cloudflare 
- Requesting so many times in Chrome driver will make the Captcha appears again -> Can close the Chrome after finishing crawling the data from 1 URL, then open it again for the next URL
## Checking the data and elements

### Data to be crawled
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/401b5667-629b-4084-bee7-a4c7471325b9)
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/87a8e5d1-eee2-4f4f-a2cc-79c83130957a)
- We can see that, from this URL, we can get the salary a year, also the minimum requirement for this position. For examples, academic degree, skills,...

### Checking elements
- For the salary, when inspecting the website, we can see that the salary is inside a div class with the class name "jobsearch-JobMetadataHeader-item"
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/23e03bce-3466-49aa-9d19-848bbb82273e)
- For the minimum requirement, these things are put inside a long text, we need to find the tag that store all these things. In here, we can find a div tag with class name "jobsearch-jobDescriptionText"
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/d40d22e3-b7cc-4375-b791-560d6de0fdad)
- After collecting all these things, we need to create some rules to get exactly what we need

## Filter for requirements
- After checking many job description, we can see that for the academic degree, there will be some keywords like: Bachelor, Master, B.C,... For the skills, some keywords will be: skills, knowledge, abilities, experience, ability, proficient,... 
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/e11c2a57-7ce9-4172-8437-00f636dd4789)

## Crawling the data
- After having all of these things, we try to crawl the job titles and job URLs, for each job related to logistics. The way to find which tag stores the job title is exactly the same as when we find the salary,...
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/53ff1455-a4af-4354-8756-37d897f79e94)
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/b5fc7a6f-cf80-4377-be68-75644302f7ef)
- Getting about 200 URLs for the logistics job, we then try to look for some required information like salary, skills, academic degree,... by using the tag we've just found.
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/73adb133-b5cc-40a6-80fc-2847e4103b35)
- After having these things, we then use the rules we've just created to get the data.

## Salary calculation 
- Some job will give the salary per year, per month or per hour. We then need to calculate these things
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/f8d05309-b7a9-4ce0-80bd-5116755b1153)

## Result
- The result will have some columns like: Job tile, Salary, Education, Experience, Skills, Job URLs and be exported as .xlsx file
![image](https://github.com/minhkhoa2404/FTU-crawl/assets/74652429/dcf1849d-ad4d-4d59-8dae-1fc7b8747c18)
