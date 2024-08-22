import json

# Load the courses.json file
with open('courses.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)
    courses = data["value"]  # Assuming your JSON structure looks like { "value": [...] }

# Initialize the list for storing insert statements
insert_statements = []

for course in courses:
    insert_statement = f"INSERT INTO Courses (ID, NAME, PROFESSOR, DAYS, STARTTIME, ENDTIME, ROOM, LAB_ROOM, INSTRUCTION_MODE, STATUS, FLAGS, CORE, LAB_DAY, LAB_STARTTIME, LAB_ENDTIME) VALUES ("
    
    insert_statement += f"{course['ID']}, "
    insert_statement += f"'{course['NAME'].replace('\'', '\'\'')}', "
    insert_statement += f"'{course['PROFESSOR'].replace('\'', '\'\'')}', "
    insert_statement += f"'{course['DAYS']}', "
    insert_statement += f"'{course['STARTTIME']}', "
    insert_statement += f"'{course['ENDTIME']}', "
    
    # Handle None for 'ROOM'
    room = course['ROOM']
    room_value = f"'{room.replace('\'', '\'\'')}'" if room else "NULL"
    insert_statement += f"{room_value}, "
    
    # Handle None for 'LAB_ROOM'
    lab_room = course['LAB_ROOM']
    lab_room_value = f"'{lab_room.replace('\'', '\'\'')}'" if lab_room else "NULL"
    insert_statement += f"{lab_room_value}, "
    
    insert_statement += f"'{course['INSTRUCTION_MODE']}', "
    insert_statement += f"'{course['STATUS']}', "
    insert_statement += f"'{course['FLAGS']}', "
    insert_statement += f"'{course['CORE']}', "
    
    # Handle None for 'LAB_DAY'
    lab_day = course['LAB_DAY']
    lab_day_value = f"'{lab_day}'" if lab_day else "NULL"
    insert_statement += f"{lab_day_value}, "
    
    # Handle None for 'LAB_STARTTIME' and 'LAB_ENDTIME'
    lab_starttime = course['LAB_STARTTIME']
    lab_starttime_value = f"'{lab_starttime}'" if lab_starttime else "NULL"
    insert_statement += f"{lab_starttime_value}, "
    
    lab_endtime = course['LAB_ENDTIME']
    lab_endtime_value = f"'{lab_endtime}'" if lab_endtime else "NULL"
    insert_statement += f"{lab_endtime_value});"
    
    insert_statements.append(insert_statement)


# Save the insert statements to a .sql file
with open('insert_courses.sql', 'w', encoding='utf-8') as sql_file:
    sql_file.write('\n'.join(insert_statements))

print("SQL Insert file created successfully.")
