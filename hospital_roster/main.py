from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from hospital_roster.database import engine, SessionLocal
from hospital_roster.models import Base, Employee, Shift

app = FastAPI()
Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    db: Session = SessionLocal()
    total = db.query(Employee).count()
    doctors = db.query(Employee).filter(Employee.role=="Doctor").count()
    nurses = db.query(Employee).filter(Employee.role=="Nurse").count()
    support = db.query(Employee).filter(Employee.role=="Supporting Staff").count()

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total": total,
        "doctors": doctors,
        "nurses": nurses,
        "support": support
    })

@app.get("/employees", response_class=HTMLResponse)
def employees(request: Request, role: str = None):
    db: Session = SessionLocal()
    if role:
        emps = db.query(Employee).filter(Employee.role==role).all()
    else:
        emps = db.query(Employee).all()

    return templates.TemplateResponse("employees.html", {
        "request": request,
        "employees": emps
    })

@app.get("/schedule", response_class=HTMLResponse)
def schedule(request: Request):
    db: Session = SessionLocal()
    shifts = db.query(Shift).limit(500).all()

    return templates.TemplateResponse("schedule.html", {
        "request": request,
        "shifts": shifts
    })
