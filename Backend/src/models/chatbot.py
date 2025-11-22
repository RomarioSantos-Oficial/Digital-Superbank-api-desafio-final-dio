from sqlalchemy import (
    Column, Integer, String, Text, DateTime,
    Float, ForeignKey, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime

from src.database.chatbot_connection import ChatbotBase


class KnowledgeBase(ChatbotBase):
    """Base de conhecimento do chatbot - Perguntas e Respostas"""
    __tablename__ = "knowledge_base"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    keywords = Column(Text)
    intent = Column(String(100), index=True)
    confidence_threshold = Column(Float, default=0.6)
    usage_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    
    variations = relationship(
        "QuestionVariation",
        back_populates="knowledge",
        cascade="all, delete-orphan"
    )


class QuestionVariation(ChatbotBase):
    """Variações de perguntas para melhorar detecção"""
    __tablename__ = "question_variations"
    
    id = Column(Integer, primary_key=True, index=True)
    knowledge_id = Column(Integer, ForeignKey("knowledge_base.id"))
    variation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    knowledge = relationship("KnowledgeBase", back_populates="variations")


class ChatConversation(ChatbotBase):
    """Histórico de conversas do chatbot"""
    __tablename__ = "chat_conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    session_id = Column(String(100), index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    
    messages = relationship(
        "ChatMessage",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )


class ChatMessage(ChatbotBase):
    """Mensagens individuais do chat"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(
        Integer, ForeignKey("chat_conversations.id")
    )
    is_user = Column(Boolean, default=True)
    message = Column(Text, nullable=False)
    detected_intent = Column(String(100), nullable=True)
    confidence_score = Column(Float, nullable=True)
    knowledge_id = Column(
        Integer, ForeignKey("knowledge_base.id"), nullable=True
    )
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    conversation = relationship("ChatConversation", back_populates="messages")
    feedback = relationship(
        "ChatFeedback", back_populates="message", uselist=False
    )


class ChatFeedback(ChatbotBase):
    """Feedback dos usuários sobre respostas do chatbot"""
    __tablename__ = "chat_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(Integer, ForeignKey("chat_messages.id"))
    is_helpful = Column(Boolean)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    message = relationship("ChatMessage", back_populates="feedback")


class UserLearnedQuestion(ChatbotBase):
    """Perguntas aprendidas dos usuários para melhorar a IA"""
    __tablename__ = "user_learned_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    session_id = Column(String(100), index=True)
    original_question = Column(Text, nullable=False)
    user_answer = Column(Text, nullable=True)
    suggested_intent = Column(String(100), nullable=True)
    suggested_category = Column(String(50), nullable=True)
    times_asked = Column(Integer, default=1)
    approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    
    
class ConversationContext(ChatbotBase):
    """Contexto da conversa para respostas mais inteligentes"""
    __tablename__ = "conversation_context"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), index=True, unique=True)
    user_id = Column(Integer, nullable=True)
    last_intent = Column(String(100), nullable=True)
    last_category = Column(String(50), nullable=True)
    context_data = Column(Text, nullable=True)  # JSON com dados do contexto
    interaction_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

