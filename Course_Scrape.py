import json
from bs4 import BeautifulSoup
import re

def clean_text(text):
    return re.sub(r'\s{2,}', ' ', text).strip()

def clean_time(time):
    return re.sub(r'[^\d:]', '', time) 

html_dir = 'htmlcourses/'

courses = []
course_id = 1  

for i in range(1, 4):
    with open(f'{html_dir}CSPage{i}.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    rows = soup.find_all('tr')

    for row in rows:
        tds = row.find_all('td')
        if len(tds) == 1 and 'course_header' in tds[0].get('class', []):
            course_name = clean_text(tds[0].find('h2').get_text())
        else:
            columns = row.find_all('td')
            if len(columns) == 0:
                continue

            # Extract span elements for times
            spans = columns[2].find_all('span')
            if len(spans) == 1:
                # Only class time
                class_time = clean_text(spans[0].get_text())
                lab_time = None
            elif len(spans) == 2:
                # Class time and lab time
                class_time = clean_text(spans[0].get_text())
                lab_time = clean_text(spans[1].get_text())
            else:
                continue

            # Extract start and end times for class and lab
            class_times = class_time.split(' ')
            start_time = clean_time(class_times[0]) if len(class_times) > 0 else ""
            end_time = clean_time(class_times[1]) if len(class_times) > 1 else ""

            lab_start_time, lab_end_time = None, None
            if lab_time:
                lab_times = lab_time.split(' ')
                lab_start_time = clean_time(lab_times[0]) if len(lab_times) > 0 else ""
                lab_end_time = clean_time(lab_times[1]) if len(lab_times) > 1 else ""

            section = {
                'NAME': course_name,
                'PROFESSOR': clean_text(columns[5].get_text()),
                'DAYS': clean_text(columns[1].get_text()),
                'STARTTIME': start_time,
                'ENDTIME': end_time,
                'ROOM': clean_text(columns[3].get_text()),
                'INSTRUCTION_MODE': clean_text(columns[4].get_text()),
                'STATUS': clean_text(columns[6].get_text()),
                'FLAGS': clean_text(columns[7].get_text()),
                'CORE': clean_text(columns[8].get_text()) if len(columns) > 8 else None,
                'PLUS': clean_text(columns[9].get_text()) if len(columns) > 9 else None,
                'ID': course_id,
                'LAB': None,
                'LAB_STARTTIME': lab_start_time,
                'LAB_ENDTIME': lab_end_time
            }

            # Check for lab details
            if re.match(r'MWF(M?)', section['DAYS']):
                section['LAB'] = 'M'
            elif re.match(r'TTh(F?)', section['DAYS']):
                section['LAB'] = 'F'

            courses.append(section)
            course_id += 1

# Convert the course data to JSON format
courses_json = json.dumps({"value": courses}, indent=4)

# Save the JSON data to a file
with open('courses.json', 'w', encoding='utf-8') as json_file:
    json_file.write(courses_json)

print('JSON file created successfully.')
