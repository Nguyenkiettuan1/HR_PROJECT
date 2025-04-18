from sqlalchemy.orm import Session
from app.models.models import User, LeaveType
from app.utils.responses import ResponseHandler
from app.schemas.users import UserResponse
from app.core.security import get_password_hash, get_token_payload, check_admin_role
import json


class leaveType:
    @staticmethod
    def get_list(db: Session, token):
        user_id = get_token_payload(token.credentials).get('id')
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise ResponseHandler.not_found_error("User", user_id)
        leaveType = db.query(LeaveType).group_by(LeaveType.id).all() or []
        return ResponseHandler.success("get list success", leaveType)
        

    @staticmethod
    def create(db: Session, token, updated_leaveType):
        user_id = get_token_payload(token.credentials).get('id')
        db_user = db.query(User).filter(User.id == user_id).first() or None
        
        if db_user is None:
            raise ResponseHandler.invalid_token("access")
        
        check_admin_role(token, db)
        
        if not db_user:
            raise ResponseHandler.not_found_error("User", user_id)
        
        if db.query(LeaveType).filter(LeaveType.type_name == updated_leaveType.type_name).first():
            raise ResponseHandler.error("Leave Type already exists")
        
        leaveType = LeaveType(id=None, **updated_leaveType.model_dump())
        db.add(leaveType)
        db.commit()
        db.refresh(leaveType)
        return ResponseHandler.success(message=None,data=leaveType)

    @staticmethod
    def edit(db: Session, token, updated_leaveType,id):
        user_id = get_token_payload(token.credentials).get('id')
        
        db_user = db.query(User).filter(User.id == user_id, User.role == 'admin').first()
        if not db_user:
           raise ResponseHandler.not_found_error("User", user_id)
       
        check_admin_role(token, db)
    
        updated_leaveType_dict = updated_leaveType.model_dump(exclude_none = True)
        db_type = db.query(LeaveType).filter(LeaveType.id == id).first()
        if not db_type:
            raise ResponseHandler.not_found_error("Leave Type", updated_leaveType.id)
        
        if db.query(LeaveType).filter(LeaveType.type_name == updated_leaveType.type_name).first():
            raise ResponseHandler.error("Leave Type already exists")
        
        for key, value in updated_leaveType_dict.items():
            setattr(db_type, key, value)
        

        db.commit()
        db.refresh(db_type)
        return ResponseHandler.update_success(db_type.type_name, db_type.id, db_type)
    
    @staticmethod
    def delele(db: Session, token,id):
        user_id = get_token_payload(token.credentials).get('id')
        
        if user_id is None :
            raise ResponseHandler.invalid_token("access")
        
        check_admin_role(token, db)

        db_type = db.query(LeaveType).filter(LeaveType.id == id).first() or None
        if db_type is None:
            raise ResponseHandler.not_found_error("Leave Type", id)
        db.delete(db_type)
        db.commit()
        return ResponseHandler.delete_success(db_type.type_name,db_type.id , db_type)