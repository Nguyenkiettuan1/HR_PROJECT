import uuid
from pydantic import BaseModel, EmailStr
from sqlalchemy import Enum
from app.schemas.leavaType import LeaveTypeOut  
from app.schemas.users import Userinfo 
from datetime import datetime, date
from typing import List, Optional

# ====== LeaveRequest Schemas ======
class BaseConfig:
    model_config = {
        "from_attributes": True , # Cho phép Pydantic lấy dữ liệu từ ORM models,
        "arbitrary_types_allowed": True  # Fix lỗi Enum không được nhận diện
    }
class LeaveRequestBase(BaseModel):
    start_date: date
    end_date: date
    reason: Optional[str] = None

class LeaveRequestCreate(LeaveRequestBase):
    class Config(BaseConfig):
        pass
        
from enum import StrEnum  # Dùng StrEnum để tương thích với Pydantic v2

class LeaveStatusEnum(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    CANCELLED = "cancelled"

class LeaveRequestOut(LeaveRequestBase):
    id: uuid.UUID
    created_at: datetime
    employee: Optional[Userinfo] = None
    leave_type: Optional[LeaveTypeOut] = None
    status: LeaveStatusEnum = LeaveStatusEnum.PENDING  # Thêm trạng thái
    class Config(BaseConfig):
        pass


class ListLeaveRequest(BaseModel):  
    message: Optional[str] = None
    data: List[LeaveRequestOut]

    class Config(BaseConfig):
        pass


class LeaveRequestResponse(BaseModel):
    message: str
    data: LeaveRequestOut

    class Config(BaseConfig):
        pass
 
