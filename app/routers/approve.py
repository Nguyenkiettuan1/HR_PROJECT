from fastapi import APIRouter, Depends, status, Header
from sqlalchemy.orm import Session
from app.schemas.approval import ApprovalCreate, ApprovalOut, ApprovalResponse
from app.db.database import get_db
from app.schemas.auth import UserOut, Signup
from app.services.approve import ApproveService


router = APIRouter(tags=["approve"], prefix="/approve")


@router.post("/change_decision", status_code=status.HTTP_200_OK, response_model=ApprovalResponse)
def change_decision(
        approveCreate : ApprovalCreate = Depends(),
        db: Session = Depends(get_db)):
    print("ok")
    return  ApproveService.change_decision_leavea_request(db, approveCreate)

