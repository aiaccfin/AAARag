# app/services/service_salestax.py
from sqlmodel import Session
from app.repositories.repository_global_type import global_type_repository

class GlobalTypeService:
    def get_all(self, session: Session):
        return global_type_repository.get_all(session)
    
global_type_service = GlobalTypeService()