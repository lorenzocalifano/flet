from passlib.context import CryptContext

# === UTILITIES DI SICUREZZA (HASHING PASSWORD) ===
# Qui usiamo bcrypt tramite passlib per gestire hash e verifica delle password.

# Configuriamo il contesto di hashing (bcrypt è sicuro e standard)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Restituisce l'hash sicuro della password in chiaro
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Confronta una password in chiaro con il suo hash e verifica se corrispondono
    return pwd_context.verify(plain_password, hashed_password)