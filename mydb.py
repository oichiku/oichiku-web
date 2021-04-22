import os

from sqlalchemy import Column, DateTime, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
ENGINE = create_engine(DB_URL)
Base = declarative_base()


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    author = Column(Text)
    title = Column(Text)
    content = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Users(Base):
    __tablename__ = "users"
    user_id = Column(Text, primary_key=True)
    name = Column(Text)
    password = Column(Text)


class Sessions(Base):
    __tablename__ = "sessions"
    sessid = Column(Text, primary_key=True)
    user_id = Column(Text)


Session = sessionmaker(bind=ENGINE)
session = Session()


def get_post(id):
    x = session.query(Posts).get(id)
    return x.author, x.title, x.content, x.created_at, x.updated_at


def get_user(user_id):
    user = session.query(Users).get(user_id)
    return user


def set_session(sessid, user_id):
    r = session.query(Sessions).filter(Sessions.user_id == user_id)
    if r:
        for s in r:
            session.delete(s)
    c = Sessions(sessid=sessid, user_id=user_id)
    session.add(c)
    session.commit()
    return 0


def get_session(sessid):
    x = session.query(Sessions).get(sessid)
    return x


if __name__ == "__main__":
    author, title, content, created_at, updated_at = get_post(0)
    print(author, title, content, created_at, updated_at)
