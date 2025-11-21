"""
Script para adicionar coluna card_brand aos cartões existentes
"""
import sys
import os

# Adiciona o diretório pai ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import text
from src.database.connection import engine, SessionLocal

def add_card_brand_column():
    """Adiciona coluna card_brand se não existir"""
    with engine.connect() as conn:
        try:
            # Verifica se a coluna já existe
            result = conn.execute(text("PRAGMA table_info(credit_cards)"))
            columns = [row[1] for row in result.fetchall()]
            
            if 'card_brand' not in columns:
                print("Adicionando coluna card_brand...")
                conn.execute(text(
                    "ALTER TABLE credit_cards ADD COLUMN card_brand VARCHAR(20) DEFAULT 'Mastercard'"
                ))
                conn.commit()
                print("✅ Coluna card_brand adicionada com sucesso!")
                
                # Atualiza cartões existentes
                db = SessionLocal()
                try:
                    db.execute(text(
                        "UPDATE credit_cards SET card_brand = 'Mastercard' WHERE card_brand IS NULL"
                    ))
                    db.commit()
                    print("✅ Cartões existentes atualizados!")
                finally:
                    db.close()
            else:
                print("ℹ️  Coluna card_brand já existe")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            conn.rollback()

if __name__ == "__main__":
    print("🔄 Iniciando migração...")
    add_card_brand_column()
    print("✅ Migração concluída!")
