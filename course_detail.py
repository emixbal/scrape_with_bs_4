from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import mysql.connector
import uuid

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="dw_scrape"
)
cursor = db.cursor(dictionary=True)

def get_all_courses_from_db():
    courses = []
    try:
        cursor.execute("SELECT id, title, sub_title, author, price, url FROM courses")
        courses_data = cursor.fetchall()

        for course_data in courses_data:
            courses.append(course_data)

        return courses

    except Exception as e:
        print(" ================ error happened ================ ")
        print(e)

def get_detail_course_from_db(course_id):
    try:
        id = (course_id,)
        qry = "SELECT id, title, sub_title, author, price, url FROM courses WHERE id = %s"
        cursor.execute(qry, id)
        course_data = cursor.fetchone()

        return course_data
    except Exception as e:
        print(" ================ error happened ================ ")
        print(e)
    # how to use it? look command bellow
    # print(get_detail_course_from_db('0bf55566-10d0-4a82-b322-65090b7db962')['url'])

# start to scraping
req_url = get_detail_course_from_db('aca0027b-d795-4c1d-a575-eb8bdf821d58')['url']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(url=req_url, headers=headers)
htmlelement = urlopen(req).read()

soup = BeautifulSoup(htmlelement, 'lxml')

curriculums = soup.find('div', class_='curriculum')

for lecture in lectures:
    lecture_data = {}
    lecture_data['']
