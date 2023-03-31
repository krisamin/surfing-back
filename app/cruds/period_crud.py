# surfing-back/app/cruds/period_crud.py

from sqlalchemy.orm import Session

from app.models.period_model import Period, PeriodInterface

def get_period(db: Session) -> str:
    current_period: PeriodInterface | None = db.query(Period).first()
    if current_period is None:
        raise Exception("Period is not set")
    return current_period.period # type: ignore