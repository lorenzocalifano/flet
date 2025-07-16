# Security utils (bcrypt, passlib)
from passlib.context import CryptContext

# Configurazione hashing (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Restituisce l'hash sicuro della password"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se la password in chiaro corrisponde all'hash"""
    return pwd_context.verify(plain_password, hashed_password)