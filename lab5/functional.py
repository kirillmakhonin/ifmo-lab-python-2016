def student_result(subjects: list, student_name: str) -> int:
    """
    Get student score
    """
    return sum(sum(p[1] for p in subj[1] if p[0] == student_name) for subj in subjects)


def get_students_names(subjects: list) -> set:
    """
    Get set of student names
    """
    return set([item[0] for sublist in subjects for item in sublist[1]])


def max_result(subjects: list) -> int:
    """
    Get max score sum of students
    """
    return max(student_result(subjects, student_name) for student_name in get_students_names(subjects))


def mark_is_5(current_mark: int, max_mark: int) -> bool:
    return current_mark >= max_mark * 0.8


def mark_is_4(current_mark: int, max_mark: int) -> bool:
    return current_mark >= max_mark * 0.6


def mark_is_3(current_mark: int, max_mark: int) -> bool:
    return current_mark >= max_mark * 0.4


def mark_is_2(current_mark: int, max_mark: int) -> bool:
    return True


def get_mark_v1(current_mark: int, max_mark: int) -> int:
    """
    First version of mark calculation
    """
    return next(i for i in (5, 4, 3, 2) if globals()['mark_is_%d' % i](current_mark, max_mark))


def get_mark_v2(current_mark: int, max_mark: int) -> int:
    """
    Second version of mark calculation
    """
    return 5 - next((i, v) for i, v in enumerate((0.8, 0.6, 0.4, -1)) if current_mark >= max_mark * v)[0]


def calculate_mark(subjects: list, student_name: str) -> int:
    """
    Calculate mark for specific student
    """
    return get_mark_v2(student_result(subjects, student_name), max_result(subjects))
    # return get_mark_v1(student_result(subjects, student_name), max_result(subjects))


def respond(subjects: list) -> list:
    """
    Build respond object (all logic inside)
    """
    return [(student_name, calculate_mark(subjects, student_name)) for student_name in list(get_students_names(subjects))]

if __name__ == '__main__':
    src = [
        ('Мат. Анализ', [('Иванов', 15), ('Петров', 13), ('Сидоров', 2), ( 'Васильев', 10), ('Жуков', 6)]),
        ('Алгебра', [('Петров', 24), ( 'Иванов', 20),( 'Васильев', 11),( 'Жуков', 12)]),
        ('Логика', [('Иванов', 10), ('Петров', 15), ('Сидоров', 6), ('Жуков', 15)])
    ]
    assert get_mark_v2(10, 11) == 5
    assert get_mark_v2(1, 11) == 2
    assert get_mark_v1(10, 11) == 5
    assert get_mark_v1(1, 11) == 2
    assert mark_is_5(10, 11)
    assert max_result(src) == 52
    assert get_students_names(src) == {'Петров', 'Иванов', 'Сидоров', 'Васильев', 'Жуков'}
    assert student_result(src, 'Иванов') == 45
    assert student_result(src, 'Сидоров') == 8
    print(respond(src))