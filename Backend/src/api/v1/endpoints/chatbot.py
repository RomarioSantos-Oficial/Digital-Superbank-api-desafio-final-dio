"""
Endpoints da API do Chatbot
BANCO DE DADOS SEPARADO: chatbot.db
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List

from src.database.chatbot_connection import get_chatbot_db
from src.api.dependencies import get_current_user_optional
from src.models.user import User
from src.schemas.chatbot import (
    ChatMessageRequest, ChatMessageResponse, ChatHistoryResponse,
    ChatFeedbackRequest, ChatFeedbackResponse, ChatStatsResponse,
    ChatHistoryItem
)
from src.services.chatbot_service import ChatbotService


router = APIRouter(prefix="/chatbot", tags=["Chatbot"])


@router.post("/message", response_model=ChatMessageResponse)
def send_message(
    request: ChatMessageRequest,
    current_user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_chatbot_db)
):
    """
    Envia mensagem para o chatbot e recebe resposta
    
    - **message**: Mensagem do usuário
    - **session_id**: ID da sessão (opcional, gerado automaticamente)
    
    Retorna:
    - **response**: Resposta do bot
    - **intent**: Intenção detectada
    - **confidence**: Confiança da resposta (0-1)
    - **session_id**: ID da sessão
    - **suggestions**: Sugestões de próximas perguntas
    """
    user_id = current_user.id if current_user else None
    
    result = ChatbotService.process_message(
        message=request.message,
        session_id=request.session_id,
        user_id=user_id,
        db=db
    )
    
    return ChatMessageResponse(**result)


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
def get_chat_history(
    session_id: str,
    db: Session = Depends(get_chatbot_db)
):
    """
    Obtém histórico completo de uma conversa
    
    - **session_id**: ID da sessão
    """
    conversation = ChatbotService.get_conversation_history(session_id, db)
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversa não encontrada"
        )
    
    messages = [
        ChatHistoryItem(
            id=msg.id,
            is_user=msg.is_user,
            message=msg.message,
            timestamp=msg.timestamp,
            intent=msg.detected_intent,
            confidence=msg.confidence_score
        )
        for msg in conversation.messages
    ]
    
    return ChatHistoryResponse(
        session_id=conversation.session_id,
        messages=messages,
        started_at=conversation.created_at,
        ended_at=conversation.ended_at
    )


@router.post("/feedback", response_model=ChatFeedbackResponse)
async def submit_feedback(
    request: ChatFeedbackRequest,
    db: Session = Depends(get_chatbot_db)
):
    """
    Envia feedback sobre uma resposta do bot
    
    - **message_id**: ID da mensagem
    - **is_helpful**: A resposta foi útil? (true/false)
    - **comment**: Comentário adicional (opcional)
    """
    success = ChatbotService.save_feedback(
        message_id=request.message_id,
        is_helpful=request.is_helpful,
        comment=request.comment,
        db=db
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mensagem não encontrada"
        )
    
    return ChatFeedbackResponse(
        success=True,
        message=(
            "Feedback registrado com sucesso! "
            "Obrigado por nos ajudar a melhorar."
        )
    )


@router.get("/stats", response_model=ChatStatsResponse)
def get_chatbot_stats(db: Session = Depends(get_chatbot_db)):
    """
    Obtém estatísticas do chatbot (admin)
    
    Retorna:
    - Total de conversas
    - Total de mensagens
    - Confiança média
    - Intenções mais usadas
    - Feedback positivo/negativo
    """
    stats = ChatbotService.get_stats(db)
    return ChatStatsResponse(**stats)


@router.get("/suggestions", response_model=List[str])
async def get_popular_questions(
    limit: int = 5,
    db: Session = Depends(get_chatbot_db)
):
    """
    Obtém perguntas mais populares/frequentes
    
    - **limit**: Número de perguntas (padrão: 5)
    """
    return ChatbotService.get_popular_questions(db, limit)


@router.get("/unanswered", response_model=List[dict])
async def get_unanswered_questions(
    limit: int = 20,
    db: Session = Depends(get_chatbot_db)
):
    """
    Obtém perguntas não respondidas para revisão
    
    - **limit**: Número de perguntas (padrão: 20)
    """
    return ChatbotService.get_unanswered_questions(db, limit)


@router.post("/learn")
async def add_knowledge(
    question: str,
    answer: str,
    category: str,
    intent: str,
    keywords: Optional[str] = None,
    db: Session = Depends(get_chatbot_db)
):
    """
    Adiciona novo conhecimento à base (aprendizado manual)
    
    - **question**: Pergunta principal
    - **answer**: Resposta
    - **category**: Categoria
    - **intent**: Intenção
    - **keywords**: Palavras-chave (separadas por vírgula)
    """
    knowledge = ChatbotService.add_learned_knowledge(
        question=question,
        answer=answer,
        category=category,
        intent=intent,
        keywords=keywords,
        db=db
    )
    
    return {
        "success": True,
        "message": "Conhecimento adicionado com sucesso!",
        "knowledge_id": knowledge.id
    }


@router.post("/learn/variation")
async def add_variation(
    knowledge_id: int,
    variation: str,
    db: Session = Depends(get_chatbot_db)
):
    """
    Adiciona variação de pergunta
    
    - **knowledge_id**: ID do conhecimento base
    - **variation**: Variação da pergunta
    """
    success = ChatbotService.add_question_variation(
        knowledge_id=knowledge_id,
        variation=variation,
        db=db
    )
    
    if success:
        return {
            "success": True,
            "message": "Variação adicionada com sucesso!"
        }
    else:
        return {
            "success": False,
            "message": "Variação já existe"
        }


@router.post("/learn/auto")
async def auto_learn_from_feedback(db: Session = Depends(get_chatbot_db)):
    """
    Executa aprendizado automático baseado em feedbacks negativos
    """
    count = ChatbotService.auto_learn_from_feedback(db)
    
    return {
        "success": True,
        "message": (
            f"Aprendizado automático concluído! "
            f"{count} novas perguntas registradas."
        ),
        "learned_count": count
    }

