from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, List, Tuple
import re
import uuid
import json
from datetime import datetime

from src.models.chatbot import (
    KnowledgeBase, QuestionVariation, ChatConversation, 
    ChatMessage, ChatFeedback, UserLearnedQuestion, ConversationContext
)
from src.models.user import User


class ChatbotService:
    
    @staticmethod
    def normalize_text(text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)  # Remove pontuação
        text = re.sub(r'\s+', ' ', text)  # Remove espaços extras
        return text.strip()
    
    @staticmethod
    def calculate_similarity(text1: str, text2: str) -> float:
        words1 = set(ChatbotService.normalize_text(text1).split())
        words2 = set(ChatbotService.normalize_text(text2).split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    @staticmethod
    def detect_intent(message: str, db: Session) -> Tuple[Optional[KnowledgeBase], float]:
        normalized_message = ChatbotService.normalize_text(message)
        
        # Busca todas as bases de conhecimento ativas
        knowledge_items = db.query(KnowledgeBase).filter(
            KnowledgeBase.is_active == True
        ).all()
        
        best_match = None
        best_score = 0.0
        
        for item in knowledge_items:
            # Compara com pergunta principal
            score = ChatbotService.calculate_similarity(normalized_message, item.question)
            
            # Compara com variações
            if item.variations:
                for variation in item.variations:
                    var_score = ChatbotService.calculate_similarity(
                        normalized_message, variation.variation
                    )
                    score = max(score, var_score)
            
            # Verifica keywords
            if item.keywords:
                keywords = [k.strip() for k in item.keywords.split(',')]
                for keyword in keywords:
                    if keyword.lower() in normalized_message:
                        score += 0.2  # Boost se keyword presente
            
            score = min(score, 1.0)  # Limita a 1.0
            
            if score > best_score:
                best_score = score
                best_match = item
        
        return best_match, best_score
    
    @staticmethod
    def get_or_create_conversation(
        session_id: Optional[str],
        user_id: Optional[int],
        db: Session
    ) -> Tuple[ChatConversation, str]:
        if not session_id:
            session_id = str(uuid.uuid4())
        
        conversation = db.query(ChatConversation).filter(
            ChatConversation.session_id == session_id
        ).first()
        
        if not conversation:
            conversation = ChatConversation(
                session_id=session_id,
                user_id=user_id
            )
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        return conversation, session_id
    
    @staticmethod
    def process_message(
        message: str,
        session_id: Optional[str],
        user_id: Optional[int],
        db: Session
    ) -> dict:
        # Obtém ou cria conversa
        conversation, session_id = ChatbotService.get_or_create_conversation(
            session_id, user_id, db
        )
        
        # Salva mensagem do usuário
        user_message = ChatMessage(
            conversation_id=conversation.id,
            is_user=True,
            message=message
        )
        db.add(user_message)
        
        # Detecta intenção
        knowledge, confidence = ChatbotService.detect_intent(message, db)
        
        if knowledge and confidence >= knowledge.confidence_threshold:
            # Resposta encontrada na base de conhecimento
            response_text = knowledge.answer
            intent = knowledge.intent
            category = knowledge.category
            
            # Atualiza contador de uso
            knowledge.usage_count += 1
            
            # Obtém sugestões relacionadas
            suggestions = ChatbotService.get_suggestions(category, db)
        else:
            # Resposta não encontrada - registra para aprendizado
            ChatbotService.learn_from_unknown_question(
                message, session_id, user_id, db
            )
            
            # Resposta padrão quando não encontra
            response_text = (
                "Desculpe, não entendi sua pergunta. "
                "Posso te ajudar com informações sobre:\n"
                "• Contas bancárias\n"
                "• Transações e PIX\n"
                "• Cartões de crédito\n"
                "• Investimentos\n"
                "• Serviços do banco\n\n"
                "Tente reformular sua pergunta!"
            )
            intent = "unknown"
            category = None
            knowledge = None
            suggestions = ChatbotService.get_popular_questions(db, limit=3)
        
        # Atualiza contexto da conversa
        ChatbotService.get_or_update_context(
            session_id, user_id, intent, category, db
        )
        
        # Salva resposta do bot
        bot_message = ChatMessage(
            conversation_id=conversation.id,
            is_user=False,
            message=response_text,
            detected_intent=intent,
            confidence_score=confidence if knowledge else 0.0,
            knowledge_id=knowledge.id if knowledge else None
        )
        db.add(bot_message)
        db.commit()
        
        return {
            "response": response_text,
            "intent": intent,
            "confidence": round(confidence, 2) if knowledge else 0.0,
            "session_id": session_id,
            "message_id": bot_message.id,
            "suggestions": suggestions
        }
    
    @staticmethod
    def get_suggestions(category: str, db: Session, limit: int = 3) -> List[str]:
        items = db.query(KnowledgeBase).filter(
            KnowledgeBase.category == category,
            KnowledgeBase.is_active == True
        ).order_by(desc(KnowledgeBase.usage_count)).limit(limit).all()
        
        return [item.question for item in items]
    
    @staticmethod
    def get_popular_questions(db: Session, limit: int = 5) -> List[str]:
        items = db.query(KnowledgeBase).filter(
            KnowledgeBase.is_active == True
        ).order_by(desc(KnowledgeBase.usage_count)).limit(limit).all()
        
        return [item.question for item in items]
    
    @staticmethod
    def get_conversation_history(session_id: str, db: Session) -> Optional[ChatConversation]:
        return db.query(ChatConversation).filter(
            ChatConversation.session_id == session_id
        ).first()
    
    @staticmethod
    def save_feedback(message_id: int, is_helpful: bool, comment: Optional[str], db: Session) -> bool:
        message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
        if not message:
            return False
        
        # Remove feedback anterior se existir
        existing = db.query(ChatFeedback).filter(
            ChatFeedback.message_id == message_id
        ).first()
        if existing:
            db.delete(existing)
        
        feedback = ChatFeedback(
            message_id=message_id,
            is_helpful=is_helpful,
            comment=comment
        )
        db.add(feedback)
        db.commit()
        return True
    
    @staticmethod
    def get_stats(db: Session) -> dict:
        total_conversations = db.query(func.count(ChatConversation.id)).scalar()
        total_messages = db.query(func.count(ChatMessage.id)).scalar()
        
        avg_confidence = db.query(
            func.avg(ChatMessage.confidence_score)
        ).filter(ChatMessage.confidence_score.isnot(None)).scalar() or 0.0
        
        # Intenções mais usadas
        most_used = db.query(
            ChatMessage.detected_intent,
            func.count(ChatMessage.id).label('count')
        ).filter(
            ChatMessage.detected_intent.isnot(None)
        ).group_by(ChatMessage.detected_intent).order_by(
            desc('count')
        ).limit(5).all()
        
        most_used_intents = [
            {"intent": intent, "count": count} for intent, count in most_used
        ]
        
        # Feedback
        feedback_positive = db.query(func.count(ChatFeedback.id)).filter(
            ChatFeedback.is_helpful == True
        ).scalar()
        
        feedback_negative = db.query(func.count(ChatFeedback.id)).filter(
            ChatFeedback.is_helpful == False
        ).scalar()
        
        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "average_confidence": round(avg_confidence, 2),
            "most_used_intents": most_used_intents,
            "feedback_positive": feedback_positive,
            "feedback_negative": feedback_negative
        }
    
    @staticmethod
    def learn_from_unknown_question(
        question: str,
        session_id: str,
        user_id: Optional[int],
        db: Session
    ) -> None:
        # Verifica se já existe
        existing = db.query(UserLearnedQuestion).filter(
            UserLearnedQuestion.original_question == question
        ).first()
        
        if existing:
            existing.times_asked += 1
            existing.session_id = session_id
        else:
            learned = UserLearnedQuestion(
                user_id=user_id,
                session_id=session_id,
                original_question=question,
                times_asked=1
            )
            db.add(learned)
        
        db.commit()
    
    @staticmethod
    def get_or_update_context(
        session_id: str,
        user_id: Optional[int],
        intent: Optional[str],
        category: Optional[str],
        db: Session
    ) -> ConversationContext:
        context = db.query(ConversationContext).filter(
            ConversationContext.session_id == session_id
        ).first()
        
        if not context:
            context = ConversationContext(
                session_id=session_id,
                user_id=user_id,
                last_intent=intent,
                last_category=category,
                interaction_count=1
            )
            db.add(context)
        else:
            context.last_intent = intent
            context.last_category = category
            context.interaction_count += 1
            context.user_id = user_id or context.user_id
        
        db.commit()
        db.refresh(context)
        return context
    
    @staticmethod
    def add_learned_knowledge(
        question: str,
        answer: str,
        category: str,
        intent: str,
        keywords: Optional[str],
        db: Session
    ) -> KnowledgeBase:
        knowledge = KnowledgeBase(
            category=category,
            question=question,
            answer=answer,
            intent=intent,
            keywords=keywords,
            is_active=True,
            usage_count=0
        )
        db.add(knowledge)
        db.commit()
        db.refresh(knowledge)
        return knowledge
    
    @staticmethod
    def add_question_variation(
        knowledge_id: int,
        variation: str,
        db: Session
    ) -> bool:
        # Verifica se já existe
        existing = db.query(QuestionVariation).filter(
            QuestionVariation.knowledge_id == knowledge_id,
            QuestionVariation.variation == variation
        ).first()
        
        if existing:
            return False
        
        var = QuestionVariation(
            knowledge_id=knowledge_id,
            variation=variation
        )
        db.add(var)
        db.commit()
        return True
    
    @staticmethod
    def get_unanswered_questions(db: Session, limit: int = 20) -> List[dict]:
        questions = db.query(UserLearnedQuestion).filter(
            UserLearnedQuestion.approved == False
        ).order_by(
            desc(UserLearnedQuestion.times_asked),
            desc(UserLearnedQuestion.created_at)
        ).limit(limit).all()
        
        return [
            {
                "id": q.id,
                "question": q.original_question,
                "times_asked": q.times_asked,
                "created_at": q.created_at.isoformat()
            }
            for q in questions
        ]
    
    @staticmethod
    def auto_learn_from_feedback(db: Session) -> int:
        # Busca mensagens com feedback negativo
        negative_feedback = db.query(ChatMessage).join(
            ChatFeedback
        ).filter(
            ChatFeedback.is_helpful == False
        ).all()
        
        learned_count = 0
        
        for message in negative_feedback:
            # Registra como pergunta não respondida
            existing = db.query(UserLearnedQuestion).filter(
                UserLearnedQuestion.original_question == message.message
            ).first()
            
            if existing:
                existing.times_asked += 1
            else:
                learned = UserLearnedQuestion(
                    user_id=None,
                    session_id="auto_learn",
                    original_question=message.message,
                    times_asked=1
                )
                db.add(learned)
                learned_count += 1
        
        db.commit()
        return learned_count
