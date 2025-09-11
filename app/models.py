from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base 
from sqlalchemy.orm import relationship 

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)  
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))  # Use appropriate type for created_at
    owner_id = Column(Integer,ForeignKey('users.id', ondelete="CASCADE"), nullable=False)  

    owner = relationship("User") #here not referencing the table here we are referencing the class wheras above in foreign key we are referencing the 
    # we are referencing the table not class 

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False) 
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    name = Column(String,nullable=False, server_default='Divyang')
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = "votes" 

    user_id = Column(Integer,ForeignKey('users.id', ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)