from fastapi import HTTPException

# Наша "зависимость" - простая функция
def verify_token(token: str)-> str:
    """
    Проверяет соответствие токена, используется с Depends
    :param token: str
    :return: str
    """
    if token != "super-secret-token":
        raise HTTPException(status_code=403, detail="Invalid Token")
    return token