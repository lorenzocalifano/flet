from sqlalchemy.orm import Session
from app.models.user import User, UserRole

# === SERVIZI PER LA GESTIONE UTENTI (DIPENDENTI) ===


def get_all_users(db: Session):
    # restituisce tutti gli utenti registrati nel sistema
    return db.query(User).all()


def create_user(db: Session, user_data):
    # aggiunge un nuovo utente al database
    # NB: la password deve essere già hashata prima di arrivare qui (gestito in auth_service)
    nuovo = User(
        nome=user_data.nome,
        cognome=user_data.cognome,
        email=user_data.email,
        password=user_data.password,
        ruolo=user_data.ruolo
    )
    db.add(nuovo)
    db.commit()
    db.refresh(nuovo)
    return nuovo


def delete_user(db: Session, user_id: int):
    # elimina un utente specifico per ID
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()


def update_user_role(db: Session, user_id: int, new_role: UserRole):
    # aggiorna il ruolo di un utente (utile per il responsabile)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.ruolo = new_role
        db.commit()
        db.refresh(user)
    return user