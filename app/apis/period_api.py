# surfing-back/app/apis/period_api.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import base_schema, auth_schema
from app.cruds import period_crud
from app.database import get_db

router = APIRouter(
    prefix="/period",
    tags=["period"],
)

@router.get("/current", responses={
    200: {"model": base_schema.GeneralSuccessResponse},
})
def current_period(
    db: Session = Depends(get_db),
):
    current_period = period_crud.get_period(db)
    return base_schema.GeneralSuccessResponse(message=current_period)