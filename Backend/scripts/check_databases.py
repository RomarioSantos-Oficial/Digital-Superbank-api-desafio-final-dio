"""
Script para verificar status dos bancos de dados
"""
import os
from src.database.connection import engine
from src.database.chatbot_connection import chatbot_engine, ChatbotSessionLocal
from src.models.chatbot import KnowledgeBase, QuestionVariation
from sqlalchemy import inspect


def check_databases():
    """Verifica status dos dois bancos de dados"""
    print("=" * 80)
    print("📊 RESUMO DOS BANCOS DE DADOS")
    print("=" * 80)
    print()
    
    # Banco principal
    print("🏦 BANCO PRINCIPAL: digital_superbank.db")
    print("   Localização: src/database/data/digital_superbank.db")
    size1 = os.path.getsize("src/database/data/digital_superbank.db")
    print(f"   Tamanho: {size1/1024:.1f} KB")
    insp1 = inspect(engine)
    tables1 = insp1.get_table_names()
    print(f"   Tabelas: {len(tables1)}")
    for i, table in enumerate(sorted(tables1), 1):
        print(f"      {i}. {table}")
    print()
    
    # Banco do chatbot
    print("🤖 BANCO DO CHATBOT: chatbot.db")
    print("   Localização: src/database/data/chatbot.db")
    size2 = os.path.getsize("src/database/data/chatbot.db")
    print(f"   Tamanho: {size2/1024:.1f} KB")
    insp2 = inspect(chatbot_engine)
    tables2 = insp2.get_table_names()
    print(f"   Tabelas: {len(tables2)}")
    for i, table in enumerate(sorted(tables2), 1):
        print(f"      {i}. {table}")
    print()
    
    # Conteúdo do chatbot
    db = ChatbotSessionLocal()
    kb_count = db.query(KnowledgeBase).count()
    var_count = db.query(QuestionVariation).count()
    db.close()
    
    print("📚 Conteúdo do Chatbot:")
    print(f"   Perguntas/Respostas: {kb_count}")
    print(f"   Variações: {var_count}")
    print()
    
    print("=" * 80)
    print("✅ SEPARAÇÃO COMPLETA!")
    print("=" * 80)
    print()
    print("💡 Vantagens:")
    print("   • Dados bancários isolados de dados do chatbot")
    print("   • Melhor organização e manutenção")
    print("   • Backup seletivo possível")
    print("   • Chatbot pode ser público (sem dados sensíveis)")
    print()


if __name__ == "__main__":
    check_databases()
