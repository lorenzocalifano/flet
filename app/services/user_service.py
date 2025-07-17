from sqlalchemy.orm import Session
from app.models.user import User, UserRole

def get_all_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user_data):
    nuovo = User(
        nome=user_data.nome,
        cognome=user_data.cognome,
        email=user_data.email,
        password=user_data.password,  # già hashato nel service auth
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

# ✅ NUOVA FUNZIONE
def update_user_role(db: Session, user_id: int, new_role: UserRole):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.ruolo = new_role
        db.commit()
        db.refresh(user)
    return user