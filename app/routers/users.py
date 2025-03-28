from fastapi import APIRouter, Depends
from app.db.database import get_db
from app.services.users import UserService
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer
from app.schemas.users import  UserResponse, UserUpdate
from fastapi.security import HTTPBearer
from app.core.security import auth_scheme
from fastapi.security.http import HTTPAuthorizationCredentials




router = APIRouter(tags=["users"], prefix="/user")
auth_scheme = HTTPBearer()


@router.get("/info", response_model=UserResponse)
def get_my_info(
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return UserService.get_my_info(db, token)

@router.post("/update", response_model=UserResponse)
def update_info(
        updated_user: UserUpdate,
        db: Session = Depends(get_db),
        token: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return UserService.edit_my_info(db, token,updated_user)