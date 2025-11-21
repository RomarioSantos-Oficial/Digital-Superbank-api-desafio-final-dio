"""
Script para popular base de conhecimento do chatbot
Adiciona perguntas, respostas e variações sobre TODAS as funcionalidades do banco
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.database.chatbot_connection import ChatbotSessionLocal
from src.models.chatbot import KnowledgeBase, QuestionVariation

def add_knowledge_item(db, category, question, answer, intent, keywords, variations=None):
    """Adiciona um item de conhecimento com suas variações"""
    kb_item = KnowledgeBase(
        category=category,
        question=question,
        answer=answer,
        intent=intent,
        keywords=keywords
    )
    db.add(kb_item)
    db.flush()  # Para obter o ID
    
    if variations:
        for var in variations:
            variation = QuestionVariation(
                knowledge_id=kb_item.id,
                variation=var
            )
            db.add(variation)
    
    print(f"✅ Adicionado: {question[:50]}...")
    return kb_item

def populate_chatbot_knowledge():
    """Popula toda a base de conhecimento"""
    db = ChatbotSessionLocal()
    
    try:
        print("🤖 Populando base de conhecimento do chatbot...")
        print("=" * 60)
        
        # ========== CONTAS BANCÁRIAS ==========
        print("\n📊 Contas Bancárias")
        
        add_knowledge_item(
            db,
            category="contas",
            question="Como criar uma nova conta?",
            answer="""Para criar uma nova conta no Digital Superbank:

1. Acesse seu perfil clicando no ícone de usuário
2. Role até a seção 'Minhas Contas'
3. Clique em 'Nova Conta'
4. Escolha o tipo de conta (Corrente, Poupança, Investimento, etc.)
5. Defina o depósito inicial (opcional)
6. Confirme a criação

Você pode ter múltiplas contas de tipos diferentes!""",
            intent="criar_conta",
            keywords="criar conta, nova conta, abrir conta, abertura conta",
            variations=[
                "Quero criar uma conta",
                "Como abrir uma conta?",
                "Posso ter mais de uma conta?",
                "Como faço para criar conta nova?",
                "Quero abrir uma conta"
            ]
        )
        
        add_knowledge_item(
            db,
            category="contas",
            question="Quais tipos de conta existem?",
            answer="""Oferecemos 7 tipos de contas:

🏦 **Conta Corrente**: Conta padrão com todas as funcionalidades
💰 **Conta Poupança**: Rendimento automático
🎓 **Conta Universitária**: Para estudantes
💼 **Conta Empresarial**: Para empresas (CNPJ)
💳 **Conta Salário**: Para recebimento de salário
📈 **Conta Investimento**: Focada em investimentos
👑 **Conta Black**: Premium com benefícios exclusivos

Cada conta tem características específicas!""",
            intent="tipos_conta",
            keywords="tipos conta, categorias conta, qual conta",
            variations=[
                "Que tipos de conta vocês tem?",
                "Quais são as contas disponíveis?",
                "Qual a diferença entre as contas?",
                "Tipos de conta"
            ]
        )
        
        add_knowledge_item(
            db,
            category="contas",
            question="Como consultar meu saldo?",
            answer="""Existem várias formas de consultar seu saldo:

📱 **No Dashboard**: O saldo total aparece no cabeçalho
📊 **Na página Contas**: Veja o saldo detalhado de cada conta
💳 **No perfil**: Seção 'Minhas Contas' mostra todas
📄 **No extrato**: Acompanhe movimentações e saldo

O saldo é atualizado em tempo real!""",
            intent="consultar_saldo",
            keywords="saldo, consultar saldo, quanto tenho, extrato",
            variations=[
                "Qual meu saldo?",
                "Quanto dinheiro eu tenho?",
                "Como ver meu saldo?",
                "Onde vejo quanto tenho na conta?",
                "Consultar saldo"
            ]
        )
        
        # ========== TRANSAÇÕES ==========
        print("\n💸 Transações")
        
        add_knowledge_item(
            db,
            category="transacoes",
            question="Como fazer um depósito?",
            answer="""Para fazer um depósito:

1. Acesse 'Transações' no menu
2. Clique em 'Depositar'
3. Selecione a conta de destino
4. Digite o valor
5. Adicione uma descrição (opcional)
6. Confirme a operação

O valor é creditado instantaneamente!

💡 Dica: Você pode fazer depósitos a qualquer hora!""",
            intent="fazer_deposito",
            keywords="deposito, depositar, adicionar dinheiro, colocar dinheiro",
            variations=[
                "Como depositar?",
                "Quero fazer um depósito",
                "Como adiciono dinheiro?",
                "Fazer depósito",
                "Depositar dinheiro"
            ]
        )
        
        add_knowledge_item(
            db,
            category="transacoes",
            question="Como fazer uma transferência?",
            answer="""Para transferir dinheiro:

1. Vá em 'Transações'
2. Clique em 'Transferir'
3. Selecione a conta de origem
4. Escolha o tipo: TED, DOC ou entre suas contas
5. Informe conta de destino (agência e número)
6. Digite o valor
7. Adicione descrição (opcional)
8. Confirme

⚡ Transferências entre suas contas são instantâneas!
📝 TED/DOC podem ter taxas dependendo do valor.""",
            intent="fazer_transferencia",
            keywords="transferencia, transferir, enviar dinheiro, ted, doc",
            variations=[
                "Como transferir?",
                "Quero transferir dinheiro",
                "Fazer transferência",
                "Enviar dinheiro para outra conta",
                "Como fazer TED?"
            ]
        )
        
        add_knowledge_item(
            db,
            category="transacoes",
            question="Como fazer um saque?",
            answer="""Para sacar dinheiro:

1. Acesse 'Transações'
2. Selecione 'Sacar'
3. Escolha a conta
4. Digite o valor (mínimo R$ 10,00)
5. Confirme a operação

💰 O saque é debitado imediatamente da sua conta.
🏧 Para saques físicos, use os caixas 24h com seu cartão.""",
            intent="fazer_saque",
            keywords="saque, sacar, retirar dinheiro",
            variations=[
                "Como sacar?",
                "Quero sacar dinheiro",
                "Fazer saque",
                "Retirar dinheiro",
                "Sacar dinheiro"
            ]
        )
        
        # ========== PIX ==========
        print("\n🔑 PIX")
        
        add_knowledge_item(
            db,
            category="pix",
            question="Como fazer um PIX?",
            answer="""Para fazer um PIX:

1. Vá em 'Transações'
2. Clique em 'PIX'
3. Escolha 'Enviar PIX'
4. Selecione sua conta
5. Digite a chave PIX do destinatário (CPF, email, telefone ou aleatória)
6. Informe o valor
7. Confirme com a senha

⚡ PIX é instantâneo e funciona 24/7!
✅ Sem taxas para transferências PIX!""",
            intent="fazer_pix",
            keywords="pix, enviar pix, transferir pix, pagamento pix",
            variations=[
                "Como faço PIX?",
                "Fazer um PIX",
                "Enviar PIX",
                "Transferir por PIX",
                "Mandar dinheiro por PIX"
            ]
        )
        
        add_knowledge_item(
            db,
            category="pix",
            question="Como cadastrar chave PIX?",
            answer="""Para cadastrar uma chave PIX:

1. Acesse seu 'Perfil' ou 'Chaves PIX' no menu
2. Clique em 'Adicionar Chave PIX'
3. Escolha o tipo:
   📱 CPF
   📧 E-mail
   📞 Telefone
   🔀 Chave Aleatória
4. Selecione a conta vinculada
5. Digite o valor da chave (ou deixe vazio para aleatória)
6. Confirme

✅ Você pode ter múltiplas chaves!
💡 Chaves facilitam receber PIX!""",
            intent="cadastrar_chave_pix",
            keywords="chave pix, cadastrar pix, criar chave, registrar pix",
            variations=[
                "Como criar chave PIX?",
                "Cadastrar chave PIX",
                "Registrar PIX",
                "Criar minha chave PIX",
                "Quero cadastrar chave PIX"
            ]
        )
        
        add_knowledge_item(
            db,
            category="pix",
            question="Quais tipos de chave PIX posso usar?",
            answer="""Você pode cadastrar 5 tipos de chave PIX:

📱 **CPF**: Seu CPF como chave
📧 **E-mail**: Seu endereço de e-mail
📞 **Telefone**: Número de celular
🏢 **CNPJ**: Para contas empresariais
🔀 **Aleatória**: Código gerado automaticamente (UUID)

💡 Dica: Você pode ter uma chave de cada tipo por conta!""",
            intent="tipos_chave_pix",
            keywords="tipos chave pix, chave pix, qual chave",
            variations=[
                "Que tipos de chave PIX existem?",
                "Quais chaves PIX posso usar?",
                "Tipos de chave PIX"
            ]
        )
        
        # ========== CARTÕES ==========
        print("\n💳 Cartões")
        
        add_knowledge_item(
            db,
            category="cartoes",
            question="Como solicitar um cartão?",
            answer="""Para solicitar seu cartão:

1. Acesse 'Cartões' no menu ou seu 'Perfil'
2. Clique em 'Solicitar Cartão'
3. Aguarde análise (normalmente instantânea)
4. Seu cartão será criado automaticamente

📦 O cartão físico chega em até 7 dias úteis
💳 Você pode usar o cartão virtual imediatamente!

⚠️ Cada usuário pode ter apenas 1 cartão.""",
            intent="solicitar_cartao",
            keywords="cartao, solicitar cartao, pedir cartao, novo cartao",
            variations=[
                "Como pedir um cartão?",
                "Quero um cartão",
                "Solicitar cartão",
                "Como consigo um cartão?",
                "Pedir cartão de crédito"
            ]
        )
        
        add_knowledge_item(
            db,
            category="cartoes",
            question="Como consultar limite do cartão?",
            answer="""Para ver o limite do seu cartão:

1. Acesse 'Cartões' no menu
2. Selecione seu cartão
3. Veja as informações:
   💰 **Limite Total**: Seu limite aprovado
   ✅ **Limite Disponível**: O que você pode usar
   📊 **Fatura Atual**: Quanto já gastou

🔄 O limite disponível é atualizado em tempo real!""",
            intent="consultar_limite_cartao",
            keywords="limite cartao, consultar limite, quanto tenho de limite",
            variations=[
                "Qual meu limite?",
                "Quanto tenho de limite no cartão?",
                "Ver limite do cartão",
                "Consultar limite"
            ]
        )
        
        add_knowledge_item(
            db,
            category="cartoes",
            question="Como bloquear meu cartão?",
            answer="""Para bloquear seu cartão em caso de perda ou roubo:

1. Acesse 'Cartões'
2. Selecione o cartão
3. Clique em 'Bloquear Cartão'
4. Confirme a ação

🔒 O bloqueio é imediato!
⚠️ Após bloqueado, você precisará solicitar um novo cartão.

💡 Em caso de roubo, faça boletim de ocorrência.""",
            intent="bloquear_cartao",
            keywords="bloquear cartao, cancelar cartao, perdi cartao",
            variations=[
                "Perdi meu cartão",
                "Quero bloquear cartão",
                "Como bloqueio o cartão?",
                "Bloquear cartão",
                "Cartão roubado"
            ]
        )
        
        # ========== INVESTIMENTOS ==========
        print("\n📈 Investimentos")
        
        add_knowledge_item(
            db,
            category="investimentos",
            question="Como investir?",
            answer="""Para começar a investir:

1. Acesse 'Investimentos' no menu
2. Escolha entre:
   📊 **Ações**: Empresas da bolsa
   🏢 **Fundos**: Fundos de investimento
3. Navegue pelos ativos disponíveis
4. Clique no ativo desejado
5. Digite a quantidade
6. Confirme a compra

💰 Você pode acompanhar seus investimentos na aba 'Meus Investimentos'!

⚠️ Invista apenas o que pode perder. Investimentos têm riscos.""",
            intent="como_investir",
            keywords="investir, investimento, comprar acao, aplicar dinheiro",
            variations=[
                "Como investir meu dinheiro?",
                "Quero investir",
                "Como comprar ações?",
                "Como funciona investimento?",
                "Começar a investir"
            ]
        )
        
        add_knowledge_item(
            db,
            category="investimentos",
            question="Quais investimentos estão disponíveis?",
            answer="""Temos diversos investimentos disponíveis:

📊 **AÇÕES** (9 opções):
   • PETR4, VALE3, ITUB4, BBDC4
   • ABEV3, MGLU3, B3SA3, WEGE3, RENT3

🏢 **FUNDOS DE INVESTIMENTO** (18 opções):
   Renda Fixa:
   • CDB (6 bancos diferentes)
   • LCI, LCA
   • Tesouro Direto (IPCA, Selic, Prefixado)
   
   Fundos:
   • Fundos DI
   • Fundos Multimercado
   • Fundos de Ações

💡 Os preços são atualizados em tempo real!""",
            intent="tipos_investimento",
            keywords="investimentos disponiveis, tipos investimento, acoes disponiveis",
            variations=[
                "Que investimentos vocês tem?",
                "Quais ações posso comprar?",
                "Tipos de investimento",
                "O que posso investir?"
            ]
        )
        
        add_knowledge_item(
            db,
            category="investimentos",
            question="Como vender meus investimentos?",
            answer="""Para vender seus investimentos:

1. Vá em 'Investimentos'
2. Acesse a aba 'Meus Investimentos'
3. Clique no investimento que deseja vender
4. Selecione 'Vender'
5. Digite a quantidade
6. Confirme a venda

💰 O dinheiro é creditado imediatamente na sua conta!
📊 Você pode vender parcialmente (apenas parte das cotas/ações).""",
            intent="vender_investimento",
            keywords="vender investimento, vender acao, resgatar investimento",
            variations=[
                "Como vender ações?",
                "Quero vender meu investimento",
                "Resgatar investimento",
                "Vender ações",
                "Como resgato?"
            ]
        )
        
        # ========== PAGAMENTOS ==========
        print("\n💵 Pagamentos")
        
        add_knowledge_item(
            db,
            category="pagamentos",
            question="Como pagar contas/boletos?",
            answer="""Para pagar contas:

1. Acesse 'Pagar Contas' no menu
2. Selecione o tipo de conta:
   💧 Água
   ⚡ Luz (Energia)
   📱 Telefone
   🌐 Internet
   🔥 Gás
   📄 Outros
3. Escolha a empresa
4. Digite o código de barras (47 dígitos)
5. Selecione a conta para débito
6. Confirme o pagamento

✅ Pagamento é instantâneo!
📜 Você pode ver o histórico na mesma página.""",
            intent="pagar_conta",
            keywords="pagar conta, pagar boleto, codigo barras, conta luz, conta agua",
            variations=[
                "Como pagar boleto?",
                "Pagar conta de luz",
                "Pagar conta de água",
                "Como pago minhas contas?",
                "Pagar fatura"
            ]
        )
        
        # ========== EXTRATO ==========
        print("\n📄 Extrato")
        
        add_knowledge_item(
            db,
            category="extrato",
            question="Como ver meu extrato completo?",
            answer="""Para ver seu extrato detalhado:

1. Clique em 'Extrato Completo' no menu
2. Você verá TODAS as transações:
   💰 Depósitos
   💸 Saques
   🔄 Transferências
   🔑 PIX (envio e recebimento)
   💳 Compras com cartão
   💵 Pagamentos de contas
   📈 Investimentos (compra e venda)

🔍 **Filtros disponíveis**:
   • Por conta
   • Por tipo de transação
   • Por período (data)

📊 O extrato mostra resumo financeiro do período!
🔄 Atualização automática a cada 30 segundos.""",
            intent="ver_extrato",
            keywords="extrato, historico, movimentacoes, transacoes",
            variations=[
                "Ver extrato",
                "Mostrar extrato",
                "Histórico de transações",
                "Minhas movimentações",
                "Extrato bancário"
            ]
        )
        
        # ========== PERFIL ==========
        print("\n👤 Perfil e Configurações")
        
        add_knowledge_item(
            db,
            category="perfil",
            question="Como alterar meus dados?",
            answer="""Para alterar seus dados:

1. Acesse 'Perfil' no menu
2. Na seção 'Informações Pessoais':
   • Nome completo
   • E-mail
   • Telefone
3. Faça as alterações
4. Clique em 'Salvar Alterações'

⚠️ **Dados que NÃO podem ser alterados**:
   • CPF
   • Data de nascimento

💡 Mantenha seus dados sempre atualizados!""",
            intent="alterar_dados",
            keywords="alterar dados, mudar email, mudar telefone, atualizar cadastro",
            variations=[
                "Como mudo meu email?",
                "Alterar dados cadastrais",
                "Mudar telefone",
                "Atualizar informações",
                "Trocar email"
            ]
        )
        
        add_knowledge_item(
            db,
            category="perfil",
            question="Como alterar minha senha?",
            answer="""Para alterar sua senha:

1. Vá em 'Perfil'
2. Na seção 'Segurança', clique em 'Alterar Senha'
3. Digite:
   • Senha atual
   • Nova senha
   • Confirme a nova senha
4. Clique em 'Alterar Senha'

🔒 **Dicas de segurança**:
   • Use senhas fortes (letras, números, símbolos)
   • Não compartilhe sua senha
   • Troque regularmente
   • Não use senhas óbvias""",
            intent="alterar_senha",
            keywords="alterar senha, mudar senha, trocar senha, esqueci senha",
            variations=[
                "Como troco minha senha?",
                "Mudar senha",
                "Esqueci a senha",
                "Redefinir senha",
                "Trocar senha"
            ]
        )
        
        # ========== SEGURANÇA ==========
        print("\n🔒 Segurança")
        
        add_knowledge_item(
            db,
            category="seguranca",
            question="O Digital Superbank é seguro?",
            answer="""Sim! Sua segurança é nossa prioridade:

🔐 **Criptografia**: Todos os dados são criptografados
🔒 **Autenticação**: Login seguro com token JWT
🛡️ **Proteção**: Firewall e sistemas anti-fraude
📱 **2FA**: Autenticação em duas etapas (em breve)
💾 **Backup**: Dados salvos com segurança

**Recomendações**:
   • Nunca compartilhe sua senha
   • Não clique em links suspeitos
   • Mantenha antivírus atualizado
   • Use redes seguras
   • Verifique sempre a URL: https://""",
            intent="seguranca",
            keywords="seguranca, seguro, protecao, criptografia",
            variations=[
                "É seguro?",
                "Meus dados estão protegidos?",
                "Como vocês protegem minha conta?",
                "Segurança do banco"
            ]
        )
        
        # ========== TAXAS ==========
        print("\n💲 Taxas e Tarifas")
        
        add_knowledge_item(
            db,
            category="taxas",
            question="Quais são as taxas?",
            answer="""📊 **Taxas do Digital Superbank**:

✅ **SEM TAXA**:
   • Abertura e manutenção de conta
   • PIX (envio e recebimento)
   • Transferências entre suas contas
   • Depósitos
   • Consultas e extratos
   • Cartão de débito (anuidade)

💳 **Cartão de Crédito**:
   • Anuidade: Isento no primeiro ano
   • Juros rotativos: 2,5% a.m.

📤 **Transferências**:
   • TED/DOC: R$ 8,00 por transação
   • TED agendado: R$ 5,00

📈 **Investimentos**:
   • Ações: Sem taxa de corretagem
   • Fundos: Conforme o fundo

Somos um banco digital, então temos menos custos e você paga menos! 🎉""",
            intent="taxas",
            keywords="taxas, tarifas, custos, quanto custa, preco",
            variations=[
                "Quanto custa?",
                "Quais as tarifas?",
                "Tem taxa?",
                "Cobram taxa de manutenção?",
                "Valores das taxas"
            ]
        )
        
        # ========== AJUDA GERAL ==========
        print("\n❓ Ajuda Geral")
        
        add_knowledge_item(
            db,
            category="ajuda",
            question="Como funciona o Digital Superbank?",
            answer="""🏦 **Digital Superbank** é seu banco digital completo!

**Principais funcionalidades**:
   📱 Múltiplas contas
   💸 Transferências e PIX
   💳 Cartão de crédito/débito
   📈 Investimentos (ações e fundos)
   💵 Pagamento de contas
   📊 Controle financeiro total
   🤖 Assistente virtual (eu!)

**Vantagens**:
   ✅ Tudo pelo celular/computador
   ✅ Sem filas
   ✅ Taxas reduzidas
   ✅ Atendimento 24/7
   ✅ Abertura de conta rápida

💡 **Navegue pelo menu** para explorar todas as funcionalidades!""",
            intent="como_funciona",
            keywords="como funciona, o que e, sobre banco, digital superbank",
            variations=[
                "O que é Digital Superbank?",
                "Como funciona?",
                "O que vocês fazem?",
                "Sobre o banco"
            ]
        )
        
        add_knowledge_item(
            db,
            category="ajuda",
            question="Onde encontro cada funcionalidade?",
            answer="""📍 **Guia de Navegação**:

🏠 **Dashboard**: Visão geral e atalhos
💼 **Contas**: Gerenciar suas contas
💸 **Transações**: Depósitos, saques, transferências
🔑 **Chaves PIX**: Gerenciar chaves PIX
💵 **Pagar Contas**: Pagamento de boletos
📄 **Extrato Completo**: Todas as movimentações
💳 **Cartões**: Seus cartões
📈 **Investimentos**: Ações e fundos
👤 **Perfil**: Dados pessoais e configurações

💡 Use o menu lateral para navegar!""",
            intent="navegacao",
            keywords="onde encontro, menu, navegacao, onde fica",
            variations=[
                "Onde fica...?",
                "Como acesso...?",
                "Onde encontro?",
                "Como navego?"
            ]
        )
        
        add_knowledge_item(
            db,
            category="ajuda",
            question="Preciso de mais ajuda",
            answer="""📞 **Canais de Atendimento**:

🤖 **Chatbot** (eu!):
   • Disponível 24/7
   • Tire dúvidas instantaneamente
   • Sem espera

📧 **E-mail**: suporte@digitalsuperbank.com
   • Resposta em até 24h

📱 **WhatsApp**: (11) 9999-9999
   • Atendimento de segunda a sexta
   • 8h às 20h

💬 **Chat ao vivo**:
   • Clique no ícone flutuante
   • Fale com um atendente

💡 **Central de Ajuda**: FAQ completo no site

Estou aqui para ajudar! Pode perguntar qualquer coisa! 😊""",
            intent="mais_ajuda",
            keywords="ajuda, suporte, contato, falar atendente",
            variations=[
                "Preciso de ajuda",
                "Falar com atendente",
                "Suporte",
                "Contato",
                "Atendimento"
            ]
        )
        
        # Commit de todas as alterações
        db.commit()
        
        print("\n" + "=" * 60)
        print("✅ Base de conhecimento populada com sucesso!")
        print(f"📚 Total de itens adicionados: {db.query(KnowledgeBase).count()}")
        print(f"🔄 Total de variações: {db.query(QuestionVariation).count()}")
        print("🤖 Chatbot pronto para uso!")
        
    except Exception as e:
        print(f"❌ Erro ao popular base: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    populate_chatbot_knowledge()
