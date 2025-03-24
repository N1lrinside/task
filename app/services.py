from sqlalchemy.orm import Session
from . import models, utils


def create_or_update_password(db: Session, service_name: str, password: str):
    encrypted_password = utils.encrypt_password(password)
    db_password = db.query(models.Password).filter(models.Password.service_name == service_name).first()
    if db_password:
        db_password.encrypted_password = encrypted_password
    else:
        db_password = models.Password(service_name=service_name, encrypted_password=encrypted_password)
        db.add(db_password)
    db.commit()
    db.refresh(db_password)
    return db_password


def get_password(db: Session, service_name: str):
    return db.query(models.Password).filter(models.Password.service_name == service_name).first()


def search_passwords(db: Session, part_name: str):
    return db.query(models.Password).filter(models.Password.service_name.contains(part_name)).all()
