"""
Script para atualizar banco de dados do chatbot com novas tabelas de aprendizado
"""
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.database.chatbot_connection import chatbot_engine, ChatbotBase
from src.models.chatbot import (
    KnowledgeBase, QuestionVariation, ChatConversation,
    ChatMessage, ChatFeedback, UserLearnedQuestion, ConversationContext
)


def update_database():
    """Cria novas tabelas no banco de dados do chatbot"""
    print("🔄 Atualizando banco de dados do chatbot...")
    
    try:
        # Cria todas as tabelas (só cria as que não existem)
        ChatbotBase.metadata.create_all(bind=chatbot_engine)
        
        print("✅ Banco de dados atualizado com sucesso!")
        print("\n📋 Novas tabelas criadas:")
        print("  • user_learned_questions - Perguntas aprendidas dos usuários")
        print("  • conversation_context - Contexto das conversas")
        print("\n🎓 Sistema de aprendizado ativo!")
        print("  • Luna agora aprende com perguntas não respondidas")
        print("  • Contexto de conversa mantido")
        print("  • Feedback usado para melhorar respostas")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar banco de dados: {e}")
        sys.exit(1)


if __name__ == "__main__":
    update_database()
