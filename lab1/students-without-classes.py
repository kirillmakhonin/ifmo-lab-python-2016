import csv

with open('students.csv', 'r') as file:
    students = [{'second_name': l[0], 'group': l[1], 'rates': [int(k) for k in l[2:]]} for l in csv.reader(file, delimiter=',')]

for _, v in enumerate(students):
    students[_]['avg_rate'] = (sum(v['rates']) + 2 * (5 - len(v['rates']))) / 5

groups = set([s['group'] for s in students])
groups = {g: [k for k in students if k['group'] == g] for g in groups}

for name, students in groups.items():
    print(name)
    students_sorted = sorted(students, key=lambda x: x['avg_rate'], reverse=True)
    for student in students_sorted:
        print("%s, %s, %s, %s" % (student['second_name'], student['group'], student['avg_rate'], ", ".join([str(r) for r in student['rates']])))

