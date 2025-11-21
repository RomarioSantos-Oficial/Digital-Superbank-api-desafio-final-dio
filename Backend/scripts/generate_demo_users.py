"""
Script para criar 20 usuários de demonstração com contas bancárias.
Salva todos os logins e senhas em pessoa.txt
"""

import sys
import os
from datetime import datetime, timedelta
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.connection import SessionLocal
from src.models.user import User
from src.models.account import Account, AccountType
from src.utils.security import get_password_hash
from src.utils.generators import generate_account_number


def generate_demo_users():
    """Gera 20 usuários de demonstração."""
    db = SessionLocal()
    
    # Lista de nomes brasileiros
    nomes = [
        ("João", "Silva"), ("Maria", "Santos"), ("Pedro", "Oliveira"),
        ("Ana", "Costa"), ("Carlos", "Rodrigues"), ("Juliana", "Almeida"),
        ("Lucas", "Ferreira"), ("Beatriz", "Pereira"), ("Rafael", "Lima"),
        ("Camila", "Souza"), ("Felipe", "Carvalho"), ("Larissa", "Ribeiro"),
        ("Gustavo", "Martins"), ("Amanda", "Gomes"), ("Bruno", "Rocha"),
        ("Patricia", "Dias"), ("Thiago", "Barbosa"), ("Fernanda", "Cardoso"),
        ("Ricardo", "Castro"), ("Vanessa", "Mendes")
    ]
    
    usuarios_criados = []
    
    print("=" * 70)
    print("🎭 CRIANDO 20 USUÁRIOS DE DEMONSTRAÇÃO")
    print("=" * 70 + "\n")
    
    try:
        for i, (nome, sobrenome) in enumerate(nomes, 1):
            # Gera CPF único
            cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
            
            # Gera email
            email = f"{nome.lower()}.{sobrenome.lower()}@superbank.com.br"
            
            # Senha padrão
            senha = f"Senha{i}@2025"
            
            # Gera telefone
            telefone = f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            
            # Gera data de nascimento (18 a 70 anos atrás)
            anos_atras = random.randint(18, 70)
            nascimento = datetime.now() - timedelta(days=anos_atras * 365)
            
            # Cria usuário
            usuario = User(
                full_name=f"{nome} {sobrenome}",
                email=email,
                cpf=cpf,
                password_hash=get_password_hash(senha),
                phone=telefone,
                birth_date=nascimento.date()
            )
            
            db.add(usuario)
            db.flush()  # Para obter o ID
            
            # Cria 3 contas para cada usuário
            contas = []
            
            # 1. Conta Corrente
            conta_corrente = Account(
                user_id=usuario.id,
                account_type=AccountType.CORRENTE,
                account_number=generate_account_number("CORRENTE"),
                agency="0001",
                balance=random.uniform(500, 50000)
            )
            db.add(conta_corrente)
            contas.append(("Corrente", conta_corrente.account_number, conta_corrente.balance))
            
            # 2. Conta Poupança
            conta_poupanca = Account(
                user_id=usuario.id,
                account_type=AccountType.POUPANCA,
                account_number=generate_account_number("POUPANCA"),
                agency="0001",
                balance=random.uniform(1000, 100000)
            )
            db.add(conta_poupanca)
            contas.append(("Poupança", conta_poupanca.account_number, conta_poupanca.balance))
            
            # 3. Conta Investimento
            conta_investimento = Account(
                user_id=usuario.id,
                account_type=AccountType.INVESTIMENTO,
                account_number=generate_account_number("INVESTIMENTO"),
                agency="0001",
                balance=random.uniform(5000, 500000)
            )
            db.add(conta_investimento)
            contas.append(("Investimento", conta_investimento.account_number, conta_investimento.balance))
            
            usuarios_criados.append({
                'numero': i,
                'nome': f"{nome} {sobrenome}",
                'email': email,
                'senha': senha,
                'cpf': cpf,
                'telefone': telefone,
                'nascimento': nascimento.date().strftime('%d/%m/%Y'),
                'contas': contas
            })
            
            print(f"✅ Usuário {i}/20: {nome} {sobrenome}")
            print(f"   Email: {email}")
            print(f"   Senha: {senha}")
            print(f"   CPF: {cpf}")
            for tipo, numero, saldo in contas:
                print(f"   Conta {tipo}: {numero} - R$ {saldo:,.2f}")
            print()
        
        # Commit no banco
        db.commit()
        
        # Salva no arquivo pessoa.txt
        arquivo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'pessoa.txt'
        )
        
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            f.write("═" * 80 + "\n")
            f.write("🏦 DIGITAL SUPERBANK - USUÁRIOS DE DEMONSTRAÇÃO\n")
            f.write("═" * 80 + "\n\n")
            f.write(f"Data de Criação: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total de Usuários: 20\n")
            f.write(f"Total de Contas: 60 (3 por usuário)\n\n")
            f.write("═" * 80 + "\n\n")
            
            for user in usuarios_criados:
                f.write(f"👤 USUÁRIO {user['numero']}/20\n")
                f.write("─" * 80 + "\n")
                f.write(f"Nome Completo: {user['nome']}\n")
                f.write(f"Email: {user['email']}\n")
                f.write(f"Senha: {user['senha']}\n")
                f.write(f"CPF: {user['cpf']}\n")
                f.write(f"Telefone: {user['telefone']}\n")
                f.write(f"Data de Nascimento: {user['nascimento']}\n\n")
                
                f.write("💳 CONTAS BANCÁRIAS:\n")
                for tipo, numero, saldo in user['contas']:
                    f.write(f"  • {tipo:12} | Nº {numero} | Saldo: R$ {saldo:>12,.2f}\n")
                
                f.write("\n" + "─" * 80 + "\n\n")
            
            f.write("═" * 80 + "\n")
            f.write("🔑 LOGIN RÁPIDO - COPIE E COLE\n")
            f.write("═" * 80 + "\n\n")
            
            for user in usuarios_criados[:5]:  # Primeiros 5 para acesso rápido
                f.write(f"{user['email']} | {user['senha']}\n")
            
            f.write("\n═" * 80 + "\n")
            f.write("✅ TODOS OS USUÁRIOS FORAM CRIADOS COM SUCESSO!\n")
            f.write("═" * 80 + "\n")
        
        print("═" * 70)
        print(f"✅ 20 USUÁRIOS CRIADOS COM SUCESSO!")
        print(f"✅ 60 CONTAS BANCÁRIAS CRIADAS!")
        print(f"✅ Dados salvos em: pessoa.txt")
        print("═" * 70)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    generate_demo_users()
