"""
Script para popular a base de conhecimento do chatbot a partir do arquivo TXT
"""
import sys
import os
from pathlib import Path
from datetime import datetime

sys.path.append('.')

from src.database.chatbot_connection import ChatbotSessionLocal
from src.models.chatbot import KnowledgeBase, QuestionVariation


def backup_file(filepath):
    """Cria backup do arquivo antes de processar"""
    if not os.path.exists(filepath):
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = filepath.replace('.txt', f'_backup_{timestamp}.txt')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return backup_path


def parse_knowledge_file(filepath):
    """Lê e parseia o arquivo de conhecimento do chatbot"""
    knowledge_items = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            
            # Ignora linhas vazias e comentários
            if not line or line.startswith('#'):
                continue
            
            # Parse do formato: CATEGORIA|PERGUNTA|RESPOSTA|PALAVRAS-CHAVE|INTENT|VARIACOES
            parts = line.split('|')
            if len(parts) != 6:
                print(f"⚠️  Linha inválida ignorada: {line[:50]}...")
                continue
            
            category, question, answer, keywords, intent, variations = parts
            
            # Processa variações (separadas por ;)
            variation_list = [v.strip() for v in variations.split(';') if v.strip()]
            
            knowledge_items.append({
                'category': category.strip(),
                'question': question.strip(),
                'answer': answer.strip().replace('\\n', '\n'),  # Converte \n literais
                'keywords': keywords.strip(),
                'intent': intent.strip(),
                'variations': variation_list
            })
    
    return knowledge_items


def populate_from_file(filepath, update_mode=False):
    """Popula base de conhecimento a partir do arquivo"""
    db = ChatbotSessionLocal()
    
    try:
        # Verifica se já existem dados
        existing_count = db.query(KnowledgeBase).count()
        if existing_count > 0:
            if update_mode:
                print(f"⚠️  Base já contém {existing_count} itens. Modo --update ativado.")
                print("🗑️  Limpando base existente...")
                db.query(QuestionVariation).delete()
                db.query(KnowledgeBase).delete()
                db.commit()
            else:
                print(f"⚠️  Base já contém {existing_count} itens!")
                print("❌ Use --update para substituir os dados existentes")
                return
        
        # Lê arquivo
        if not os.path.exists(filepath):
            print(f"❌ Arquivo não encontrado: {filepath}")
            return
        
        print(f"📖 Lendo arquivo: {filepath}")
        knowledge_items = parse_knowledge_file(filepath)
        
        if not knowledge_items:
            print("❌ Nenhum item válido encontrado no arquivo!")
            return
        
        print(f"📊 {len(knowledge_items)} itens encontrados")
        print()
        print("=" * 80)
        print("POPULANDO BASE DE CONHECIMENTO DO CHATBOT")
        print("=" * 80)
        print()
        
        # Popula banco
        categories_count = {}
        
        for idx, item_data in enumerate(knowledge_items, 1):
            variations = item_data.pop('variations', [])
            category = item_data['category']
            
            # Cria item de conhecimento
            kb_item = KnowledgeBase(**item_data)
            db.add(kb_item)
            db.flush()  # Para obter o ID
            
            # Adiciona variações
            for variation_text in variations:
                variation = QuestionVariation(
                    knowledge_id=kb_item.id,
                    variation=variation_text
                )
                db.add(variation)
            
            # Contabiliza categorias
            categories_count[category] = categories_count.get(category, 0) + 1
            
            # Mostra progresso
            question_preview = item_data['question'][:60]
            print(f"✅ [{idx:2d}/{len(knowledge_items)}] {category:15s} | {question_preview}")
        
        db.commit()
        
        print()
        print("=" * 80)
        print("✅ BASE DE CONHECIMENTO POPULADA COM SUCESSO!")
        print("=" * 80)
        print()
        print(f"📊 Total de itens: {len(knowledge_items)}")
        print()
        print("📚 Distribuição por categorias:")
        for cat, count in sorted(categories_count.items()):
            print(f"   • {cat.capitalize():15s}: {count:2d} itens")
        print()
        print("🤖 O chatbot está pronto para uso!")
        print("   Endpoint: POST /api/v1/chatbot/message")
        print()
        print(f"💾 Arquivo fonte: {filepath}")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao popular base de conhecimento: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Popular base de conhecimento do chatbot')
    parser.add_argument(
        '--update', 
        action='store_true',
        help='Atualiza dados existentes (substitui tudo)'
    )
    parser.add_argument(
        '--file',
        default='../demo/chatbot_conhecimento.txt',
        help='Caminho do arquivo (padrão: ../demo/chatbot_conhecimento.txt)'
    )
    
    args = parser.parse_args()
    
    # Resolve caminho relativo
    script_dir = Path(__file__).parent.parent
    filepath = script_dir / args.file
    
    print()
    print("=" * 80)
    print("POPULAR BASE DE CONHECIMENTO DO CHATBOT")
    print("=" * 80)
    print()
    
    if not args.update:
        print("⚠️  ATENÇÃO: Este script irá popular a base de conhecimento do chatbot")
        print("   a partir do arquivo TXT.")
        print()
        print(f"   Arquivo: {filepath}")
        print()
        
        existing_db = ChatbotSessionLocal()
        existing_count = existing_db.query(KnowledgeBase).count()
        existing_db.close()
        
        if existing_count > 0:
            print(f"   ⚠️  Já existem {existing_count} itens na base!")
            print("   ❌ Use --update para substituir os dados existentes")
            print()
            sys.exit(0)
    
    populate_from_file(str(filepath), args.update)
