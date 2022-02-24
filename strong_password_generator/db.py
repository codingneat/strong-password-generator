import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine, select
from sqlalchemy.orm import relationship, backref, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database

load_dotenv()

Base = declarative_base()


class Site(Base):
    __tablename__ = "site"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    passwords = relationship(
        "Password", backref=backref("site")
    )

class Password(Base):
    __tablename__ = "password"
    id = Column(Integer, primary_key=True)
    password = Column(String)
    site_id = Column(Integer, ForeignKey("site.id"))
    created_at = Column(DateTime)


def get_engine():
    engine = create_engine(os.environ.get("SQLITE_DATABASE"))
    if not database_exists(engine.url):
        create_database(engine.url)
        Base.metadata.create_all(bind=engine)
    return engine


def add_password(site_name, password):
    engine = get_engine()
    with Session(engine) as session:
        db_site = session.execute(select(Site).filter(Site.name == site_name)).first()
        password = Password(
            password= password,
            site= db_site[0] if db_site else Site(name=site_name),
            created_at = datetime.now()
        )

        session.add(password)
        session.commit()


def get_passwords(site_name):
    engine = get_engine()
    with Session(engine) as session:
        return session.execute(select(Password.password, Password.created_at)
            .join(Site.passwords).filter(Site.name == site_name).order_by(Password.created_at.desc())).all()

