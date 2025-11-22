from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.configs.settings import settings

# Engine separada para o chatbot
chatbot_engine = create_engine(
    settings.CHATBOT_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session local para chatbot
ChatbotSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=chatbot_engine
)

# Base separada para models do chatbot
ChatbotBase = declarative_base()


def get_chatbot_db():
    db = ChatbotSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_chatbot_tables():
    ChatbotBase.metadata.create_all(bind=chatbot_engine)
