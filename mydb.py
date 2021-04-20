from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os


DB_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
ENGINE = create_engine(DB_URL)
Base = declarative_base()


class Posts(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    content = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


Session = sessionmaker(bind=ENGINE)
session = Session()


def get_post(id):
    x = session.query(Posts).get(id)
    return x.title, x.content, x.created_at, x.updated_at


if __name__ == "__main__":
    title, content, created_at, updated_at = get_post(0)
    print(title, content, created_at, updated_at)
