from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, database
from .schemas import PasswordCreate, PasswordResponse

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post(
    "/password/{service_name}",
    response_model=PasswordResponse
)
def create_password(
        service_name: str,
        password: PasswordCreate,
        db: Session = Depends(get_db)
) -> PasswordResponse:
    db_password = crud.create_or_update_password(db, service_name, password.password)
    return PasswordResponse(
        service_name=db_password.service_name,
        password=password.password
    )


@app.get(
    "/password/{service_name}",
    response_model=PasswordResponse
)
def read_password(
        service_name: str,
        db: Session = Depends(get_db)
) -> PasswordResponse:
    db_password = crud.get_password(db, service_name)
    if db_password is None:
        raise HTTPException(status_code=404, detail="Service not found")
    return PasswordResponse(
        service_name=db_password.service_name,
        password=db_password.encrypted_password
    )


@app.get(
    "/password/",
    response_model=list[PasswordResponse]
)
def search_password(
        service_name: str,
        db: Session = Depends(get_db)
) -> list[PasswordResponse]:
    passwords = crud.search_passwords(db, service_name)
    return [
        PasswordResponse(service_name=p.service_name, password=p.encrypted_password)
        for p in passwords
    ]
