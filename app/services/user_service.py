from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.utils.security import hash_password

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user_data):
    nuovo = User(
        nome=user_data.nome,
        cognome=user_data.cognome,
        email=user_data.email,
        password=hash_password(user_data.password),
        ruolo=user_data.ruolo
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()