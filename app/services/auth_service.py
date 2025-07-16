# Authentication service
from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.utils.security import hash_password, verify_password
from app.schemas.user_schema import UserCreate
from sqlalchemy.exc import IntegrityError

def register_user(db: Session, user_data: UserCreate):
    """Registra un nuovo utente"""
    new_user = User(
        nome=user_data.nome,
        cognome=user_data.cognome,
        email=user_data.email,
        password=hash_password(user_data.password),
        ruolo=user_data.ruolo
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email già registrata")

def authenticate_user(db: Session, email: str, password: str):
    """Autentica un utente tramite email e password"""
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user