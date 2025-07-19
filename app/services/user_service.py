from sqlalchemy.orm import Session
from app.models.user import User, UserRole
from app.utils.security import hash_password
from app.schemas.user_schema import UserCreate
from app.services.email_service import send_email  # <-- Usa il servizio email già creato

def get_all_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user_data: UserCreate):
    """Crea un nuovo utente e invia automaticamente le credenziali via email"""
    nuovo = User(
        nome=user_data.nome,
        cognome=user_data.cognome,
        email=user_data.email,
        password=hash_password(user_data.password),  # Password hashata
        ruolo=user_data.ruolo
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)

    # Invio mail con le credenziali solo se la creazione è andata a buon fine
    try:
        subject = "Credenziali di accesso al Gestionale Magazzino"
        body = (
            f"Ciao {nuovo.nome} {nuovo.cognome},\n\n"
            f"Il tuo account è stato creato con successo.\n\n"
            f"Credenziali di accesso:\n"
            f"Email: {nuovo.email}\n"
            f"Password: {user_data.password}\n\n"
            f"-- Gestionale Magazzino"
        )
        send_email(nuovo.email, subject, body)
        print(f"Email inviata a {nuovo.email}")
    except Exception as e:
        print(f"Errore nell'invio dell'email a {nuovo.email}: {e}")

    return nuovo


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()


def update_user_role(db: Session, user_id: int, new_role: UserRole):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.ruolo = new_role
        db.commit()
        db.refresh(user)
    return user