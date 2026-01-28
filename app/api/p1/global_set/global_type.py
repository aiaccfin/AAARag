from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from app.db.connection.conn_rls import get_tenant_session, tenant_role_session_dependency, tenant_session_dependency
from app.models.rls.m_global_type_rls import TypeDB, TypeCreate, TypeRead
import uuid
from app.services.service_global_type import global_type_service

router = APIRouter()
TENANT_ID = "550e8400-e29b-41d4-a716-446655440000"


@router.get("/", response_model=list[TypeRead])
async def list_generic_store(session: Session = Depends(tenant_session_dependency(TENANT_ID))):
    return global_type_service.get_all(session)


@router.post("/", response_model=TypeRead)
async def create_generic(data: TypeCreate,    session: Session = Depends(tenant_session_dependency(TENANT_ID))):

    # Make SQLModel instance
    new_generic = TypeDB(**data.dict(), tenant_id=TENANT_ID)

    session.add(new_generic)
    session.commit()
    session.refresh(new_generic)

    return new_generic

