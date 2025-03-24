from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from . import services
from .schemas import PasswordCreate, PasswordResponse
from .database import get_db

router = APIRouter(prefix="/password", tags=["Passwords"],)


@router.post(
    "/{service_name}",
    response_model=PasswordResponse
)
def create_password(
        service_name: str,
        password: PasswordCreate,
        db: Session = Depends(get_db)
) -> PasswordResponse:
    db_password = services.create_or_update_password(db, service_name, password.password)
    return PasswordResponse(
        service_name=db_password.service_name,
        password=password.password
    )


@router.get(
    "/{service_name}",
    response_model=PasswordResponse
)
def read_password(
        service_name: str,
        db: Session = Depends(get_db)
) -> PasswordResponse:
    db_password = services.get_password(db, service_name)
    if db_password is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return PasswordResponse(
        service_name=db_password.service_name,
        password=db_password.encrypted_password
    )


@router.get(
    "/",
    response_model=list[PasswordResponse]
)
def search_password(
        service_name: str,
        db: Session = Depends(get_db)
) -> list[PasswordResponse]:
    passwords = services.search_passwords(db, service_name)
    return [
        PasswordResponse(service_name=p.service_name, password=p.encrypted_password)
        for p in passwords
    ]