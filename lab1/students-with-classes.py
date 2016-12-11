import csv


class Student:
    """
    Student information
    """

    def __init__(self, second_name, group, *rates):
        self.second_name = second_name
        self.group = group
        self.rates = [int(rate) for rate in rates]

    @property
    def avg_rate(self):
        rate_sum = sum(self.rates) + 2 * (5 - len(self.rates))
        return rate_sum / 5

    def __str__(self):
        return "%s, %s, %s, %s" % (self.second_name, self.group, self.avg_rate, ", ".join([str(r) for r in self.rates]))

    __repr__ = __str__


class Group:
    """
    Group information (with students)
    """

    def __init__(self, id):
        self.id = id
        self.students = []

    def add_student(self, student_info):
        self.students.append(student_info)

    @property
    def sorted_students(self):
        return sorted(self.students, key=lambda x: x.avg_rate, reverse=True)

    def __repr__(self):
        return "Group %s. Students: %s" % (self.id, ", ".join([s.second_name for s in self.students]))

    __str__ = __repr__


def task_1():
    with open('students.csv', 'r') as file:
        students = [Student(*l) for l in csv.reader(file, delimiter=',')]

    groups = set([s.group for s in students])
    groups = {g: Group(g) for g in groups}

    for student in students:
        groups[student.group].add_student(student)

    for name, group in groups.items():
        print(name)

        for student in group.sorted_students:
            print(student)

if __name__ == '__main__':
    task_1()