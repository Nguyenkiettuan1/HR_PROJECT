import uuid
from pydantic import BaseModel, EmailStr
from datetime import datetime, date
from typing import List, Optional

from app.models.models import LeaveRequest
# from app.schemas.leavaRequest import LeaveRequestOut
from app.schemas.users import UserOut



# ====== Approval Schemas ======
class ApprovalBase(BaseModel):
    decision: str
    comments: Optional[str] = None


class ApprovalCreate(ApprovalBase):
    leave_request_id: uuid.UUID
    approver_id: uuid.UUID


class ApprovalOut(ApprovalBase):
    id: uuid.UUID
    decision_date: datetime
    leave_request: LeaveRequest
    approver_id: str

    model_config = {
        "from_attributes": True,  # Cách mới
        "arbitrary_types_allowed": True  # Cho phép kiểu tùy ý
    }
        
class ApprovalResponse(BaseModel):
    data: str
    message: str
    status: str
