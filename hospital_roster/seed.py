import random
from datetime import date, timedelta
from hospital_roster.database import SessionLocal
from hospital_roster.models import Employee, Shift
db = SessionLocal()

roles = (
    ["Doctor"] * 50 +
    ["Nurse"] * 150 +
    ["Supporting Staff"] * 100
)

random.shuffle(roles)

# Create Employees
for i in range(300):
    emp = Employee(
        name=f"Employee_{i+1}",
        role=roles[i]
    )
    db.add(emp)

db.commit()

employees = db.query(Employee).all()

shift_types = ["Morning", "Evening", "Night"]

start_date = date(2026, 1, 1)
end_date = date(2026, 12, 31)

for emp in employees:
    current = start_date
    while current <= end_date:
        week = [current + timedelta(days=i) for i in range(7)]
        offs = random.sample(week, 2)

        for d in week:
            if d > end_date:
                break
            shift = "Off" if d in offs else random.choice(shift_types)

            db.add(Shift(
                employee_id=emp.id,
                date=d,
                shift_type=shift
            ))

        current += timedelta(days=7)

db.commit()
print("Database Seeded Successfully")
