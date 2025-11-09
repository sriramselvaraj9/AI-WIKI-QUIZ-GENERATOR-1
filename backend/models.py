from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from database import Base


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(2048), nullable=False)
    title = Column(String(512), nullable=True)
    date_generated = Column(DateTime(timezone=True), server_default=func.now())
    scraped_content = Column(Text, nullable=True)
    full_quiz_data = Column(Text, nullable=True)  # JSON string

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "date_generated": self.date_generated.isoformat() if self.date_generated else None,
            "scraped_content": self.scraped_content,
            "full_quiz_data": self.full_quiz_data,
        }