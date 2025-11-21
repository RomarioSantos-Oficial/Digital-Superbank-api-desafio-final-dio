"""
Script para criar usuários com diferentes modalidades de contas.
Gera perfis variados: apenas corrente, corrente+poupança, universitária, etc.
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


def generate_varied_users():
    """Gera usuários com diferentes modalidades de contas."""
    db = SessionLocal()
    
    # Perfis variados com idades e tipos de conta adequados
    # REGRA: TODOS devem ter conta corrente obrigatória
    perfis = [
        # Perfil 1: Universitário (18-25 anos) - Corrente Universitária
        {
            'nome': 'Gabriel', 'sobrenome': 'Souza',
            'idade': 19,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (100, 2000), 'descricao': 'Corrente Universitária'}
            ]
        },
        {
            'nome': 'Isabella', 'sobrenome': 'Martins',
            'idade': 21,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (200, 3000), 'descricao': 'Corrente Universitária'}
            ]
        },
        
        # Perfil 2: Jovem trabalhador (22-30) - Apenas Corrente
        {
            'nome': 'Mateus', 'sobrenome': 'Alves',
            'idade': 24,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (1000, 8000), 'descricao': 'Corrente'}
            ]
        },
        {
            'nome': 'Letícia', 'sobrenome': 'Costa',
            'idade': 27,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (2000, 12000), 'descricao': 'Corrente'}
            ]
        },
        
        # Perfil 3: Profissional estabelecido (30-45) - Corrente + Poupança
        {
            'nome': 'Rodrigo', 'sobrenome': 'Fernandes',
            'idade': 35,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (5000, 25000), 'descricao': 'Corrente'},
                {'tipo': AccountType.POUPANCA, 'saldo': (10000, 80000), 'descricao': 'Poupança'}
            ]
        },
        {
            'nome': 'Carla', 'sobrenome': 'Ribeiro',
            'idade': 38,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (8000, 30000), 'descricao': 'Corrente'},
                {'tipo': AccountType.POUPANCA, 'saldo': (15000, 100000), 'descricao': 'Poupança'}
            ]
        },
        
        # Perfil 4: Investidor iniciante (25-40) - Corrente + Investimento
        {
            'nome': 'Daniel', 'sobrenome': 'Moreira',
            'idade': 29,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (3000, 15000), 'descricao': 'Corrente'},
                {'tipo': AccountType.INVESTIMENTO, 'saldo': (5000, 50000), 'descricao': 'Investimento'}
            ]
        },
        {
            'nome': 'Aline', 'sobrenome': 'Barros',
            'idade': 32,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (4000, 20000), 'descricao': 'Corrente'},
                {'tipo': AccountType.INVESTIMENTO, 'saldo': (10000, 80000), 'descricao': 'Investimento'}
            ]
        },
        
        # Perfil 5: Poupador conservador (45-60) - Corrente + Poupança (alta)
        {
            'nome': 'Sérgio', 'sobrenome': 'Lopes',
            'idade': 52,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (2000, 10000), 'descricao': 'Corrente'},
                {'tipo': AccountType.POUPANCA, 'saldo': (50000, 200000), 'descricao': 'Poupança'}
            ]
        },
        {
            'nome': 'Márcia', 'sobrenome': 'Dias',
            'idade': 48,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (3000, 15000), 'descricao': 'Corrente'},
                {'tipo': AccountType.POUPANCA, 'saldo': (60000, 250000), 'descricao': 'Poupança'}
            ]
        },
        
        # Perfil 6: Investidor avançado (35-55) - Corrente + Poupança + Investimento
        {
            'nome': 'Eduardo', 'sobrenome': 'Santos',
            'idade': 42,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (10000, 40000), 'descricao': 'Corrente'},
                {'tipo': AccountType.POUPANCA, 'saldo': (30000, 150000), 'descricao': 'Poupança'},
                {'tipo': AccountType.INVESTIMENTO, 'saldo': (100000, 500000), 'descricao': 'Investimento'}
            ]
        },
        {
            'nome': 'Sandra', 'sobrenome': 'Oliveira',
            'idade': 45,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (15000, 50000), 'descricao': 'Corrente'},
                {'tipo': AccountType.POUPANCA, 'saldo': (40000, 200000), 'descricao': 'Poupança'},
                {'tipo': AccountType.INVESTIMENTO, 'saldo': (150000, 600000), 'descricao': 'Investimento'}
            ]
        },
        
        # Perfil 7: Aposentado (60+) - Corrente + Poupança + Investimento
        {
            'nome': 'José', 'sobrenome': 'Silva',
            'idade': 65,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (5000, 20000), 'descricao': 'Corrente'},
                {'tipo': AccountType.POUPANCA, 'saldo': (80000, 300000), 'descricao': 'Poupança'},
                {'tipo': AccountType.INVESTIMENTO, 'saldo': (200000, 800000), 'descricao': 'Investimento'}
            ]
        },
        {
            'nome': 'Helena', 'sobrenome': 'Rodrigues',
            'idade': 62,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (8000, 30000), 'descricao': 'Corrente'},
                {'tipo': AccountType.POUPANCA, 'saldo': (100000, 400000), 'descricao': 'Poupança'},
                {'tipo': AccountType.INVESTIMENTO, 'saldo': (250000, 900000), 'descricao': 'Investimento'}
            ]
        },
        
        # Perfil 8: Recém-chegado (18) - Apenas Corrente básica
        {
            'nome': 'Lucas', 'sobrenome': 'Pereira',
            'idade': 18,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (50, 500), 'descricao': 'Corrente Básica'}
            ]
        },
        
        # Perfil 9: Freelancer (25-35) - Corrente com alto volume
        {
            'nome': 'Marina', 'sobrenome': 'Cardoso',
            'idade': 28,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (15000, 60000), 'descricao': 'Corrente MEI'}
            ]
        },
        
        # Perfil 10: Empresário (40-60) - Todas as contas com altos valores
        {
            'nome': 'Roberto', 'sobrenome': 'Mendes',
            'idade': 48,
            'contas': [
                {'tipo': AccountType.CORRENTE, 'saldo': (50000, 200000), 'descricao': 'Corrente Empresarial'},
                {'tipo': AccountType.POUPANCA, 'saldo': (100000, 400000), 'descricao': 'Poupança'},
                {'tipo': AccountType.INVESTIMENTO, 'saldo': (500000, 2000000), 'descricao': 'Investimento Premium'}
            ]
        },
    ]
    
    usuarios_criados = []
    usuario_num = 21  # Começa do 21 pois já existem 20
    
    print("=" * 70)
    print("🎭 CRIANDO USUÁRIOS COM PERFIS VARIADOS")
    print("=" * 70 + "\n")
    
    try:
        for i, perfil in enumerate(perfis, 1):
            nome = perfil['nome']
            sobrenome = perfil['sobrenome']
            idade = perfil['idade']
            
            # Gera CPF único
            cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
            
            # Gera email
            email = f"{nome.lower()}.{sobrenome.lower()}@superbank.com.br"
            
            # Senha padrão
            senha = f"Senha{usuario_num}@2025"
            
            # Gera telefone
            telefone = f"(11) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"
            
            # Calcula data de nascimento baseada na idade
            hoje = datetime.now()
            nascimento = hoje - timedelta(days=idade * 365 + random.randint(0, 365))
            
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
            db.flush()
            
            # Cria contas conforme o perfil
            contas_info = []
            for conta_config in perfil['contas']:
                tipo_map = {
                    AccountType.CORRENTE: "CORRENTE",
                    AccountType.POUPANCA: "POUPANCA",
                    AccountType.INVESTIMENTO: "INVESTIMENTO"
                }
                
                conta = Account(
                    user_id=usuario.id,
                    account_type=conta_config['tipo'],
                    account_number=generate_account_number(tipo_map[conta_config['tipo']]),
                    agency="0001",
                    balance=random.uniform(*conta_config['saldo'])
                )
                db.add(conta)
                
                contas_info.append({
                    'tipo': conta_config['descricao'],
                    'numero': conta.account_number,
                    'saldo': conta.balance
                })
            
            usuarios_criados.append({
                'numero': usuario_num,
                'nome': f"{nome} {sobrenome}",
                'email': email,
                'senha': senha,
                'cpf': cpf,
                'telefone': telefone,
                'nascimento': nascimento.date().strftime('%d/%m/%Y'),
                'idade': idade,
                'contas': contas_info,
                'perfil': f"Perfil {i}"
            })
            
            print(f"✅ Usuário {usuario_num}/{usuario_num + len(perfis) - 1}: {nome} {sobrenome}")
            print(f"   Idade: {idade} anos")
            print(f"   Email: {email}")
            print(f"   Senha: {senha}")
            print(f"   CPF: {cpf}")
            print(f"   Perfil: {len(perfil['contas'])} conta(s)")
            for conta in contas_info:
                print(f"   • {conta['tipo']}: {conta['numero']} - R$ {conta['saldo']:,.2f}")
            print()
            
            usuario_num += 1
        
        # Commit no banco
        db.commit()
        
        # Atualiza arquivo pessoa.txt
        arquivo_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'pessoa.txt'
        )
        
        # Lê conteúdo existente
        with open(arquivo_path, 'r', encoding='utf-8') as f:
            conteudo_existente = f.read()
        
        # Remove a parte final (após LOGIN RÁPIDO)
        if '🔑 LOGIN RÁPIDO' in conteudo_existente:
            conteudo_base = conteudo_existente.split('🔑 LOGIN RÁPIDO')[0]
        else:
            conteudo_base = conteudo_existente
        
        # Adiciona novos usuários
        with open(arquivo_path, 'w', encoding='utf-8') as f:
            f.write(conteudo_base)
            
            for user in usuarios_criados:
                f.write(f"👤 USUÁRIO {user['numero']}\n")
                f.write("─" * 80 + "\n")
                f.write(f"Nome Completo: {user['nome']}\n")
                f.write(f"Email: {user['email']}\n")
                f.write(f"Senha: {user['senha']}\n")
                f.write(f"CPF: {user['cpf']}\n")
                f.write(f"Telefone: {user['telefone']}\n")
                f.write(f"Data de Nascimento: {user['nascimento']} ({user['idade']} anos)\n\n")
                
                f.write("💳 CONTAS BANCÁRIAS:\n")
                for conta in user['contas']:
                    f.write(f"  • {conta['tipo']:20} | Nº {conta['numero']} | Saldo: R$ {conta['saldo']:>12,.2f}\n")
                
                f.write("\n" + "─" * 80 + "\n\n")
            
            f.write("═" * 80 + "\n")
            f.write("📊 RESUMO DE PERFIS\n")
            f.write("═" * 80 + "\n\n")
            f.write("⚠️  REGRA: TODOS os usuários possuem Conta Corrente obrigatória!\n\n")
            f.write("1. Universitários (18-25 anos): Corrente Universitária\n")
            f.write("2. Jovens trabalhadores (22-30): Apenas Corrente\n")
            f.write("3. Profissionais (30-45): Corrente + Poupança\n")
            f.write("4. Investidores iniciantes (25-40): Corrente + Investimento\n")
            f.write("5. Poupadores (45-60): Corrente + Poupança (alta)\n")
            f.write("6. Investidores avançados (35-55): Completo (3 contas)\n")
            f.write("7. Aposentados (60+): Corrente + Poupança + Investimento\n")
            f.write("8. Recém-chegados (18): Corrente básica\n")
            f.write("9. Freelancers (25-35): Corrente MEI\n")
            f.write("10. Empresários (40-60): Todas com altos valores\n\n")
            
            f.write("═" * 80 + "\n")
            f.write("✅ TOTAL: 37 USUÁRIOS COM PERFIS VARIADOS!\n")
            f.write("═" * 80 + "\n")
        
        print("═" * 70)
        print(f"✅ {len(usuarios_criados)} USUÁRIOS CRIADOS COM PERFIS VARIADOS!")
        print(f"✅ Arquivo pessoa.txt atualizado!")
        print("═" * 70)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    generate_varied_users()
