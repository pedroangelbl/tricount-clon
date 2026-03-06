import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.member import Member
from app.schemas.member import MemberResponse, MemberCreate, MemberUpdate


router = APIRouter(prefix="/members", tags=["Members"])

@router.get("", response_model=list[MemberResponse])
def get_all(db: Session = Depends(get_db)):
    return db.query(Member).all()
    
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: uuid.UUID, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member

@router.post("", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    db_member = Member(
        display_name=member.display_name,
        group_id=member.group_id
    )

    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member
    
@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: uuid.UUID, updated_member: MemberUpdate, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    
    # Solo actualizar los campos que vienen
    if updated_member.display_name is not None:
        member.display_name = updated_member.display_name
    
    db.commit()
    db.refresh(member)
    return member   