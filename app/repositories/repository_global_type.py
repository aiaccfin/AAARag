# app/repositories/gst_repository.py
from sqlmodel import Session, select
from app.models.rls.m_global_type_rls import TypeDB

class GlobalTypeRepository:
    def get_all(self, session: Session):
        statement = select(TypeDB)
        return session.exec(statement).all()

global_type_repository = GlobalTypeRepository()