import csv
from pathlib import Path

from models import Director, Guard, School, Teacher


def main() -> None:
    school = School("Школа №89")
    school.employees = [
        Director("Мельник", "Олена", "Василівна", teaching_years=28, management_years=12),
        Teacher("Шевчук", "Андрій", "Миколайович", teaching_years=15),
        Teacher("Бондар", "Наталія", "Іванівна", teaching_years=22),
        Teacher("Гнатюк", "Олег", "Романович", teaching_years=9),
        Teacher("Савчук", "Тетяна", "Олегівна", teaching_years=31),
        Teacher("Кравчук", "Віктор", "Степанович", teaching_years=18),
        Teacher("Литвин", "Оксана", "Богданівна", teaching_years=6),
        Teacher("Поліщук", "Марина", "Юріївна", teaching_years=25),
        Guard("Остапчук", "Василь", "Петрович", work_years=14),
    ]

    rows: list[list[str]] = []
    print(f"{'Посада':<10} {'ПІБ':<30} {'Зарплата, грн':>14}")
    for employee in school.employees:
        salary = employee.calculate_salary()  # у кожної посади своя формула
        print(f"{employee.position:<10} {employee.full_name():<30} {salary:>14.2f}")
        rows.append([employee.position, employee.full_name(), f"{salary:.2f}"])

    Path("output").mkdir(exist_ok=True)
    with open("output/salaries.csv", "w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Посада", "ПІБ", "Зарплата, грн"])
        writer.writerows(rows)
    print("Таблицю збережено у файл output/salaries.csv")


if __name__ == "__main__":
    main()
