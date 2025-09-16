from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_ , and_ ,extract
from app.models.contacts import Contact
from app.schemas.contacts import ContactCreate, ContactUpdate
from datetime import date, timedelta

def get_contact(db: Session, contact_id:int) -> Optional[Contact]:
    return db.query(Contact).filter(Contact.id == contact_id).first()


def get_contacts(db: Session, skip: int = 0, limit: int = 100, search: Optional[str] = None) -> List[Contact]:
    query = db.query(Contact)
    if search:
        search_filter = or_(
            Contact.first_name.ilike(f"%{search}%"),
            Contact.last_name.ilike(f"%{search}%"),
            Contact.email.ilike(f"%{search}%")
        )
        query = query.filter(search_filter)
    return query.offset(skip).limit(limit).all()
    

def create_contact(db:Session, contact: ContactCreate) -> Contact:
    db_contact = Contact(**contact.model_dump())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def update_contact(db:Session, contact_id:int, contact_update: ContactUpdate) -> Optional[Contact]:
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return None
    update_data = contact_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_contact, field, value)

    db.commit()
    db.refresh(db_contact)
    return db_contact


def delete_contact(db:Session, contact_id:int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        return False
    
    db.delete(db_contact)
    db.commit()
    return True

def get_contacts_with_upcoming_birthdays(db: Session) -> List[Contact]:
    today = date.today()
    next_week = today + timedelta(days=7)
    if today.year == next_week.year:
        return db.query(Contact).filter(
            and_(
                extract('month', Contact.birth_date) >= today.month,
                extract('month', Contact.birth_date) <= next_week.month,
                or_(
                    extract('month', Contact.birth_date) > today.month,
                    and_(
                        extract('month', Contact.birth_date) == today.month, 
                        extract('day', Contact.birth_date) >= today.day 
                    )
                ),
                or_(
                    extract('month', Contact.birth_date) < next_week.month, 
                    and_(
                        extract('month', Contact.birth_date) == next_week.month,
                        extract('day', Contact.birth_date) <= next_week.day 
                    )
                )
            )
        ).all()
    else:
        return db.query(Contact).filter(
            or_(
                and_(
                    extract('month', Contact.birth_date) == today.month,
                    extract('day', Contact.birth_date) >= today.day
                ), 
                and_(
                    extract('month', Contact.birth_date) == next_week.month,
                    extract('day', Contact.birth_date) <= next_week.day
                )
            )
        ).all()          
             