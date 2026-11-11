import csv
from abc import ABC, abstractmethod


# Базовий клас для людини: тут тільки ПІБ, бо воно є і в учнів, і в працівників
class Person:
    def __init__(self, last_name: str, first_name: str, patronymic: str) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic

    # повертає ПІБ одним рядком
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}"


# Учень, ПІБ береться з Person
class Student(Person):
    def __init__(self, last_name: str, first_name: str, patronymic: str,
                 birth_year: int, gender: str, average_grade: float) -> None:
        super().__init__(last_name, first_name, patronymic)
        self.birth_year = birth_year
        self.gender = gender  # "Ч" або "Ж"
        self.average_grade = average_grade


# Клас у школі, наприклад 7А
class SchoolClass:
    def __init__(self, grade: int, letter: str) -> None:
        self._grade = grade  # паралель (1-11), змінюється лише через promote()
        self.letter = letter  # вертикаль (А, Б, В...)
        self.students: list[Student] = []

    # паралель можна тільки прочитати
    @property
    def grade(self) -> int:
        return self._grade

    # назва класу, наприклад "7А"
    @property
    def name(self) -> str:
        return f"{self._grade}{self.letter}"

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    # переводимо клас на рік вперед: 7А стає 8А, учні ті самі
    def promote(self) -> None:
        self._grade += 1

    # щоб len(клас) повертав кількість учнів
    def __len__(self) -> int:
        return len(self.students)


# Працівник школи. Клас абстрактний, тому напряму його не створити,
# тільки через конкретну посаду. Тут спільне для всіх посад: ПІБ і базова ставка,
# а формулу зарплати кожна посада пише сама
class Employee(Person, ABC):
    position = ""

    def __init__(self, last_name: str, first_name: str, patronymic: str,
                 base_salary: float) -> None:
        super().__init__(last_name, first_name, patronymic)
        self.base_salary = base_salary

    # у кожної посади своя формула зарплати
    @abstractmethod
    def calculate_salary(self) -> float:
        pass


# Директор: ставка 15000, рахується педстаж і стаж керування
class Director(Employee):
    position = "Директор"

    def __init__(self, last_name: str, first_name: str, patronymic: str,
                 teaching_years: int, management_years: int,
                 base_salary: float = 15000) -> None:
        super().__init__(last_name, first_name, patronymic, base_salary)
        self.teaching_years = teaching_years
        self.management_years = management_years

    # ставка * педстаж / 50 + стаж керування * 500
    def calculate_salary(self) -> float:
        return self.base_salary * self.teaching_years / 50 + self.management_years * 500


# Вчитель: ставка 12000, рахується тільки педстаж
class Teacher(Employee):
    position = "Вчитель"

    def __init__(self, last_name: str, first_name: str, patronymic: str,
                 teaching_years: int, base_salary: float = 12000) -> None:
        super().__init__(last_name, first_name, patronymic, base_salary)
        self.teaching_years = teaching_years

    # ставка * педстаж / 30
    def calculate_salary(self) -> float:
        return self.base_salary * self.teaching_years / 30


# Охоронець: ставка 11000 + доплата за досвід
class Guard(Employee):
    position = "Охоронець"

    def __init__(self, last_name: str, first_name: str, patronymic: str,
                 work_years: int, base_salary: float = 11000) -> None:
        super().__init__(last_name, first_name, patronymic, base_salary)
        self.work_years = work_years

    # ставка + досвід * 250
    def calculate_salary(self) -> float:
        return self.base_salary + self.work_years * 250


# Школа: тут зберігаються всі класи і працівники, її використовують обидва сценарії
class School:
    def __init__(self, name: str) -> None:
        self.name = name
        self.classes: list[SchoolClass] = []
        self.employees: list[Employee] = []

    # шукаємо клас за паралеллю і літерою, якщо нема - None
    def get_class(self, grade: int, letter: str) -> SchoolClass | None:
        for school_class in self.classes:
            if school_class.grade == grade and school_class.letter == letter:
                return school_class
        return None

    # всі учні школи одним списком
    def all_students(self) -> list[Student]:
        return [student for school_class in self.classes for student in school_class.students]

    # виводимо статистику по пунктах a-e із завдання.
    # sizes - це список кількості учнів у кожному класі, з нього беремо max, min і середнє
    def print_statistics(self) -> None:
        students = self.all_students()
        total = len(students)
        boys = sum(1 for student in students if student.gender == "Ч")
        sizes = [len(school_class) for school_class in self.classes]
        # якщо однаковий максимум чи мінімум у кількох класів - виводимо всі
        largest = [c.name for c in self.classes if len(c) == max(sizes)]
        smallest = [c.name for c in self.classes if len(c) == min(sizes)]
        boys_percent = boys / total * 100
        print(f"a) Загальна кількість учнів: {total}")
        print(f"b) Хлопці: {boys_percent:.1f} %, дівчата: {100 - boys_percent:.1f} %")
        print(f"c) Середня кількість учнів у класі: {total / len(self.classes):.1f}")
        print(f"d) Максимальна кількість учнів: {max(sizes)} ({', '.join(largest)})")
        print(f"e) Мінімальна кількість учнів: {min(sizes)} ({', '.join(smallest)})")

    def promote_all_classes(self) -> None:
        # 11-ті класи випускаються, тому просто прибираємо їх зі списку,
        # а всі інші класи переводимо на рік вперед. Після цього 1-х класів не буде
        self.classes = [c for c in self.classes if c.grade < 11]
        for school_class in self.classes:
            school_class.promote()


# Читаємо два CSV файли і створюємо з них школу з класами та учнями
def load_school(name: str, classes_file: str, students_file: str) -> School:
    school = School(name)
    # спочатку класи
    with open(classes_file, encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            school.classes.append(SchoolClass(int(row["grade"]), row["letter"]))

    # потім учні: в кожному рядку є паралель і літера класу,
    # по них знаходимо потрібний клас і додаємо туди учня
    with open(students_file, encoding="utf-8-sig") as file:
        for row in csv.DictReader(file):
            student = Student(row["last_name"], row["first_name"], row["patronymic"],
                              int(row["birth_year"]), row["gender"],
                              float(row["average_grade"]))
            school_class = school.get_class(int(row["grade"]), row["letter"])
            if school_class is not None:
                school_class.add_student(student)
    return school
