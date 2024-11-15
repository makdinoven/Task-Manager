from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..schemas import User, UserCreate
from ..crud import get_user_by_username, create_user, get_user_by_id
from ..dependencies import get_db, get_current_user
from ..auth import create_access_token, verify_password, get_password_hash
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

# Регистрация пользователя
@router.post("/signup", response_model=User)
def create_user_signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    # Вызываем функцию из crud.py для создания пользователя
    return create_user(db=db, user=user)
# Авторизация пользователя
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Смена пароля пользователя
@router.post("/change-password")
def change_password(
    new_password: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    hashed_password = get_password_hash(new_password)
    db_user = get_user_by_id(db, user_id=current_user.id)
    db_user.hashed_password = hashed_password
    db.commit()
    return {"message": "Password updated successfully"}
