import bcrypt

def verify_password(plain, hashed):
    password_byte_enc = plain.encode('utf-8')
    return bcrypt.checkpw(password=password_byte_enc, hashed_password=hashed)


def get_password_hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password

a = get_password_hash('123')
print(verify_password('13', a))