import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.group import Group
from app.schemas.group import GroupCreate, GroupUpdate, GroupResponse


router = APIRouter(prefix="/groups", tags=["Groups"])

@router.get("", response_model=list[GroupResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(Group).all()
    
@router.get("/{group_id}", response_model=GroupResponse)
def get_group(group_id: uuid.UUID, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.post("", response_model=GroupResponse)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = Group(
        name=group.name,
        description=group.description,
        created_by=group.created_by
    )

    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    return db_group
    
@router.put("/{group_id}", response_model=GroupResponse)
def update_group(group_id: uuid.UUID, updated_group: GroupUpdate, db: Session = Depends(get_db)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Solo actualizar los campos que vienen
    if updated_group.name is not None:
        # validar que no exista otro con ese email
        group.name = updated_group.name
        
    if updated_group.description is not None:
        group.description = updated_group.description
    
    db.commit()
    db.refresh(group)
    return group   