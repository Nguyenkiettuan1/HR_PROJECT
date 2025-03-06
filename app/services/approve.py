from app.models.models import Approval, LeaveRequest, User
from app.schemas.approval import ApprovalCreate
from app.utils.responses import ResponseHandler
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import logging

logging.basicConfig(level=logging.DEBUG)
class ApproveService:
    
    @staticmethod
    def change_decision_leavea_request(db: Session, approveCreate: ApprovalCreate):
        
            # 1. Kiểm tra Leave Request có tồn tại không
            leave_request = db.query(LeaveRequest).filter(LeaveRequest.id == approveCreate.leave_request_id).first()
            if not leave_request:
                logging.error("Leave request not found")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Leave request not found")

            # 2. Kiểm tra Approver có tồn tại không
            approver = db.query(User).filter(User.id == approveCreate.approver_id).first()
            if not approver:
                logging.error("Approver not found")
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Approver not found")

            
            # 4. Cập nhật trạng thái của Leave Request
            logging.info(f"Updating leave request {leave_request.id} status to {approveCreate.decision}")
            leave_request.status = approveCreate.decision
            db.commit()

            # 5. Lưu vào bảng Approvals
            approve = Approval(**approveCreate.model_dump())  
            db.add(approve)
            db.commit()
            db.refresh(approve)

            return ResponseHandler.responseEntity("ok", "Approval updated successfully", status.HTTP_200_OK)