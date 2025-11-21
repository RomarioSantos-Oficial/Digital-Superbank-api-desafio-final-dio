"""
Schemas Pydantic para o sistema de Chatbot
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ChatMessageRequest(BaseModel):
    """Requisição de mensagem do usuário"""
    message: str = Field(..., min_length=1, max_length=1000, description="Mensagem do usuário")
    session_id: Optional[str] = Field(None, description="ID da sessão (gerado automaticamente se não fornecido)")


class ChatMessageResponse(BaseModel):
    """Resposta do chatbot"""
    response: str = Field(..., description="Resposta do bot")
    intent: Optional[str] = Field(None, description="Intenção detectada")
    confidence: Optional[float] = Field(None, description="Confiança da resposta (0-1)")
    session_id: str = Field(..., description="ID da sessão")
    suggestions: Optional[List[str]] = Field(default=[], description="Sugestões de próximas perguntas")
    
    class Config:
        from_attributes = True


class ChatHistoryItem(BaseModel):
    """Item do histórico de chat"""
    id: int
    is_user: bool
    message: str
    timestamp: datetime
    intent: Optional[str] = None
    confidence: Optional[float] = None
    
    class Config:
        from_attributes = True


class ChatHistoryResponse(BaseModel):
    """Histórico completo de uma conversa"""
    session_id: str
    messages: List[ChatHistoryItem]
    started_at: datetime
    ended_at: Optional[datetime] = None


class ChatFeedbackRequest(BaseModel):
    """Feedback sobre uma resposta"""
    message_id: int = Field(..., description="ID da mensagem")
    is_helpful: bool = Field(..., description="A resposta foi útil?")
    comment: Optional[str] = Field(None, max_length=500, description="Comentário adicional")


class ChatFeedbackResponse(BaseModel):
    """Confirmação de feedback"""
    success: bool
    message: str
    
    class Config:
        from_attributes = True


class KnowledgeBaseItem(BaseModel):
    """Item da base de conhecimento"""
    id: int
    category: str
    question: str
    answer: str
    keywords: Optional[str] = None
    intent: str
    usage_count: int
    
    class Config:
        from_attributes = True


class KnowledgeBaseCreateRequest(BaseModel):
    """Criar novo item na base de conhecimento (admin)"""
    category: str = Field(..., max_length=50)
    question: str = Field(..., min_length=5, max_length=500)
    answer: str = Field(..., min_length=10, max_length=2000)
    keywords: Optional[str] = Field(None, description="Palavras-chave separadas por vírgula")
    intent: str = Field(..., max_length=100)
    variations: Optional[List[str]] = Field(default=[], description="Variações da pergunta")


class ChatStatsResponse(BaseModel):
    """Estatísticas do chatbot"""
    total_conversations: int
    total_messages: int
    average_confidence: float
    most_used_intents: List[dict]
    feedback_positive: int
    feedback_negative: int
