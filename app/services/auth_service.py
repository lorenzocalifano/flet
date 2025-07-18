from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.utils.security import hash_password, verify_password
from app.schemas.user_schema import UserCreate
from sqlalchemy.exc import IntegrityError

def register_user(db: Session, user_data: UserCreate):
    # registra un nuovo utente nel database
    new_user = User(
        nome=user_data.nome,
        cognome=user_data.cognome,
        email=user_data.email,
        password=hash_password(user_data.password),  # hashiamo subito la password
        ruolo=user_data.ruolo
    )
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        # email già presente nel db
        db.rollback()
        raise ValueError("Email già registrata")


def authenticate_user(db: Session, email: str, password: str):
    # controlla se le credenziali sono corrette
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        # email inesistente o password sbagliata
        return None
    return user