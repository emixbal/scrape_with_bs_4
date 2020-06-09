from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import mysql.connector
import uuid

db = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="dw_scrape"
)

req_url = ''
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
req = Request(url=req_url, headers=headers)
htmlelement = urlopen(req).read()

soup = BeautifulSoup(htmlelement, 'lxml')

courses_data = soup.find_all('div', class_='course-listing')
courses = []

for course_data in courses_data:
    course = {}
    course['id'] = str(uuid.uuid4())
    course['title'] = course_data.find('div', class_='course-listing-title').get_text().replace('\n','').strip()
    course['sub_title'] = course_data.find('div', class_='course-listing-subtitle').get_text().replace('\n','').strip()
    course['author'] = course_data.find('div', class_='course-author-name').get_text().replace('\n','').strip()
    course['price'] = course_data.find('div', class_='course-price').get_text().replace('\n','').replace('Rp','').replace(',','').strip()
    course['url'] = 'yourtargeturl.com'+course_data.find('a', href=True)['href']

    courses.append(course)

print(courses)
print(" ================= STORE DATA INTO DB ================= ")

cursor = db.cursor()
print(cursor)

try:
    cursor.executemany("""
        INSERT INTO courses (id, title, sub_title, author, price, url)
        VALUES (%(id)s, %(title)s, %(sub_title)s, %(author)s, %(price)s, %(url)s)
        """, courses)
    db.commit()
    print(" ================= STORE DATA INTO DB IS SUCCEED ================= ")

except Exception as e:
    print(" ================= STORE DATA INTO DB IS FAILED ================= ")
    print(e)
