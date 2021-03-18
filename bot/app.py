import time
import json
from bs4 import BeautifulSoup
from selenium import webdriver as wb
from config import EMAIL, PASSWORD

driver = wb.Chrome(
    executable_path='D:\selenium\chromedriver_win32\chromedriver.exe')

driver.maximize_window()

driver.get('https://www.linkedin.com')
time.sleep(1)

input_email = driver.find_element_by_id('session_key')
input_email.send_keys(EMAIL)
time.sleep(1)

input_password = driver.find_element_by_id('session_password')
input_password.send_keys(PASSWORD)
time.sleep(1)

submit_button = driver.find_element_by_xpath(
    '/html/body/main/section[1]/div[2]/form/button')
submit_button.click()
time.sleep(1)

driver.get('https://www.linkedin.com/school/jadavpur-university/people/')

# Scroll to get all data


def scrollToEnd():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(3)
    height = driver.execute_script("return document.body.scrollHeight")
    flag = True

    while(flag):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if(new_height == height):
            flag = False
        height = new_height


driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
time.sleep(4)
# scrollToEnd()

# Get Alumni handle

alumni_list = driver.find_elements_by_class_name(
    'org-people-profile-card__profile-info')

print(alumni_list[0])


def getAlumniDetails(alumni_handle_link):
    time.sleep(1)
    driver.get(alumni_handle_link)
    time.sleep(3)
    src = driver.page_source
    soup = BeautifulSoup(src, features="html.parser")

    name_div = soup.find('div', {'class': 'flex-1 mr5'})
    image_div = soup.find('div', {'class': 'pv-top-card__photo-wrapper ml0'})
    exp_section = soup.find('section', {'id': 'experience-section'})
    edu_section = soup.find('section', {'id': 'education-section'})

    name = name_div.find_all('ul')[0].find('li').get_text().strip()
    loc = name_div.find_all('ul')[1].find('li').get_text().strip()
    profile_title = name_div.find('h2').get_text().strip()
    image = image_div.find('img')['src']

    exp_a = exp_section.find('ul').find('div').find('a')
    job_title = exp_a.find('h3').get_text().strip()
    company_name = exp_a.find_all('p')[1].get_text().strip()
    date_employed = exp_a.find_all('h4')[0].find_all('span')[
        1].get_text().strip()
    employment_duration = exp_a.find_all('h4')[1].find_all('span')[
        1].get_text().strip()

    edu_a = edu_section.find('ul').find('div').find('a')
    institute_name = edu_a.find('h3').get_text().strip()
    degree_name = edu_a.find_all('p')[0].find_all('span')[1].get_text().strip()
    field_of_study = edu_a.find_all('p')[1].find_all('span')[
        1].get_text().strip()
    started = edu_a.find_all('time')[0].get_text().strip()
    completed = edu_a.find_all('time')[1].get_text().strip()

    alumni_details = {
        "name": name,
        "address": loc,
        "profile_title": profile_title,
        "image": image,
        "experience": {
            "company_name": company_name,
            "job_title": job_title,
            "date_employed": date_employed,
            "employment_duration": employment_duration
        },
        "education": {
            "institute_name": institute_name,
            "degree_name": degree_name,
            "field_of_study": field_of_study,
            "started": started,
            "completed": completed
        }
    }

    return alumni_details


alumni_detail_list = []

for alumni_info in alumni_list:
    alumni_handle = alumni_info.find_element_by_tag_name(
        'a').get_attribute('href')

    alumni_detail_list.append(getAlumniDetails(alumni_handle))


with open("output.json", "w") as outfile:
    json.dump(alumni_detail_list, outfile)
