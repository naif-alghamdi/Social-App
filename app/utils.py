from passlib.context import CryptContext# this is used to hash the password

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # create a CryptContext object to hash the password

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
