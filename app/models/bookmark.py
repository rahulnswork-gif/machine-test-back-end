from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    repo_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    html_url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_login = Column(String, nullable=False)
    owner_avatar_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="bookmarks")
