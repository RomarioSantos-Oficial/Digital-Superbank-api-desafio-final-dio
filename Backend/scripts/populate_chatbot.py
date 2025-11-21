"""
Script para popular a base de conhecimento do chatbot
"""
import sys
sys.path.append('.')

from src.database.connection import SessionLocal
from src.models.chatbot import KnowledgeBase, QuestionVariation


def populate_knowledge_base():
    """Popula base de conhecimento com perguntas frequentes"""
    db = SessionLocal()
    
    try:
        # Verifica se já existem dados
        existing = db.query(KnowledgeBase).first()
        if existing:
            print("⚠️  Base de conhecimento já contém dados")
            response = input("Deseja adicionar mais dados? (s/n): ")
            if response.lower() != 's':
                return
        
        knowledge_items = [
            # ===== CATEGORIA: CONTAS =====
            {
                "category": "contas",
                "question": "Como abrir uma conta?",
                "answer": "Para abrir uma conta no Digital Superbank:\n1. Faça seu cadastro em /api/v1/auth/register\n2. Faça login em /api/v1/auth/login\n3. Crie sua conta em /api/v1/accounts/\n\nTemos 7 tipos de contas: Corrente, Poupança, Salário, Universitária, Empresarial, Investimento e Black.",
                "keywords": "abrir, criar, nova, conta, cadastro",
                "intent": "abrir_conta",
                "variations": [
                    "Quero abrir uma conta",
                    "Como faço para criar conta",
                    "Preciso de uma conta nova"
                ]
            },
            {
                "category": "contas",
                "question": "Quais tipos de contas existem?",
                "answer": "Oferecemos 7 tipos de contas:\n\n1. **Corrente** - Conta básica para todos\n2. **Poupança** - Com rendimento automático\n3. **Salário** - Para recebimento de salário\n4. **Universitária** - Para estudantes (18-25 anos)\n5. **Empresarial** - Para empresas\n6. **Investimento** - Para investir (requer Black ou Empresarial)\n7. **Black** - Premium (mínimo R$ 50.000)",
                "keywords": "tipos, contas, quais, categorias",
                "intent": "tipos_conta",
                "variations": [
                    "Que contas vocês têm",
                    "Tipos de conta disponíveis",
                    "Quais contas posso abrir"
                ]
            },
            {
                "category": "contas",
                "question": "Como consultar meu saldo?",
                "answer": "Para consultar seu saldo:\n\nFaça uma requisição GET para:\n/api/v1/accounts/{id}/balance\n\nVocê precisará estar autenticado e fornecer o ID da sua conta. Você pode listar suas contas em /api/v1/accounts/",
                "keywords": "saldo, consultar, ver, quanto tenho",
                "intent": "consultar_saldo",
                "variations": [
                    "Quanto tenho de saldo",
                    "Ver meu saldo",
                    "Checar saldo da conta"
                ]
            },
            {
                "category": "contas",
                "question": "O que é Conta Black?",
                "answer": "A Conta Black é nossa conta premium que exige saldo mínimo de R$ 50.000,00.\n\nVantagens:\n• Atendimento prioritário\n• Taxas diferenciadas\n• Limite maior para transações\n• Acesso a investimentos exclusivos\n\nPara validar se sua conta atende aos requisitos, use: GET /api/v1/accounts/{id}/validate-black",
                "keywords": "black, premium, vip, especial",
                "intent": "info_conta_black",
                "variations": [
                    "Conta Black o que é",
                    "Benefícios conta Black",
                    "Como ter conta Black"
                ]
            },
            
            # ===== CATEGORIA: TRANSAÇÕES =====
            {
                "category": "transacoes",
                "question": "Como fazer um depósito?",
                "answer": "Para fazer um depósito:\n\nPOST /api/v1/transactions/deposit\n\nEnvie:\n{\n  \"account_id\": 123,\n  \"amount\": 1000.00,\n  \"description\": \"Depósito inicial\"\n}\n\nO valor será creditado imediatamente na sua conta!",
                "keywords": "depositar, deposito, adicionar dinheiro",
                "intent": "fazer_deposito",
                "variations": [
                    "Quero depositar",
                    "Como adiciono dinheiro",
                    "Fazer um depósito"
                ]
            },
            {
                "category": "transacoes",
                "question": "Como fazer um saque?",
                "answer": "Para fazer um saque:\n\nPOST /api/v1/transactions/withdraw\n\nLimites:\n• R$ 2.000 por operação\n• 3 saques por dia\n• R$ 5.000 total por dia\n\nEnvie:\n{\n  \"account_id\": 123,\n  \"amount\": 500.00,\n  \"description\": \"Saque\"\n}",
                "keywords": "sacar, saque, retirar",
                "intent": "fazer_saque",
                "variations": [
                    "Quero sacar dinheiro",
                    "Como retiro dinheiro",
                    "Fazer saque"
                ]
            },
            {
                "category": "transacoes",
                "question": "Qual o limite de saque?",
                "answer": "Limites de saque:\n\n• **Por operação:** R$ 2.000,00\n• **Saques por dia:** Máximo 3\n• **Total diário:** R$ 5.000,00\n\nEstes limites são para sua segurança!",
                "keywords": "limite, saque, quanto posso, maximo",
                "intent": "limite_saque",
                "variations": [
                    "Quanto posso sacar",
                    "Limite de saque diário",
                    "Máximo de saque"
                ]
            },
            {
                "category": "transacoes",
                "question": "Como fazer uma transferência?",
                "answer": "Para fazer transferência entre contas:\n\nPOST /api/v1/transactions/transfer\n\nEnvie:\n{\n  \"from_account_id\": 123,\n  \"to_account_number\": \"12345-6\",\n  \"amount\": 100.00,\n  \"description\": \"Transferência\"\n}\n\nA transferência é instantânea!",
                "keywords": "transferir, transferencia, enviar",
                "intent": "fazer_transferencia",
                "variations": [
                    "Quero transferir",
                    "Como envio dinheiro",
                    "Fazer transferência"
                ]
            },
            {
                "category": "transacoes",
                "question": "Como fazer PIX?",
                "answer": "Para enviar PIX:\n\nPOST /api/v1/transactions/pix/send\n\nEnvie:\n{\n  \"from_account_id\": 123,\n  \"pix_key\": \"11999999999\",\n  \"amount\": 50.00,\n  \"description\": \"PIX\"\n}\n\nO PIX é instantâneo e funciona 24/7!",
                "keywords": "pix, enviar pix, transferencia pix",
                "intent": "fazer_pix",
                "variations": [
                    "Quero fazer um PIX",
                    "Como envio PIX",
                    "Transferir via PIX"
                ]
            },
            {
                "category": "transacoes",
                "question": "Como pagar um boleto?",
                "answer": "Para pagar boleto:\n\nPOST /api/v1/transactions/pay-bill\n\nEnvie:\n{\n  \"account_id\": 123,\n  \"bar_code\": \"23791234500000100009876543210\",\n  \"amount\": 150.00,\n  \"description\": \"Conta de luz\"\n}\n\nO pagamento é processado na hora!",
                "keywords": "boleto, pagar boleto, conta",
                "intent": "pagar_boleto",
                "variations": [
                    "Quero pagar um boleto",
                    "Como pago boleto",
                    "Pagar conta"
                ]
            },
            {
                "category": "transacoes",
                "question": "Como ver meu extrato?",
                "answer": "Para ver seu extrato:\n\nGET /api/v1/transactions/statement?account_id=123\n\nVocê pode filtrar por:\n• Data inicial e final\n• Tipo de transação\n• Ordenação\n\nO extrato mostra todas suas movimentações!",
                "keywords": "extrato, historico, movimentacoes",
                "intent": "ver_extrato",
                "variations": [
                    "Quero ver o extrato",
                    "Mostrar histórico",
                    "Minhas movimentações"
                ]
            },
            
            # ===== CATEGORIA: CARTÕES =====
            {
                "category": "cartoes",
                "question": "Como solicitar um cartão de crédito?",
                "answer": "Para solicitar cartão de crédito:\n\nPOST /api/v1/credit-cards/\n\nEnvie:\n{\n  \"account_id\": 123,\n  \"requested_limit\": 5000.00\n}\n\nFazemos análise automática de crédito baseada no seu score!\n\nCategorias disponíveis:\n• **Basic** - Até R$ 5.000\n• **Platinum** - Até R$ 15.000\n• **Black** - Até R$ 50.000",
                "keywords": "cartao, credito, solicitar",
                "intent": "solicitar_cartao",
                "variations": [
                    "Quero um cartão",
                    "Como peço cartão de crédito",
                    "Solicitar cartão"
                ]
            },
            {
                "category": "cartoes",
                "question": "Quais bandeiras de cartão vocês aceitam?",
                "answer": "Trabalhamos com 4 bandeiras:\n\n• **Visa**\n• **Mastercard**\n• **Elo**\n• **American Express**\n\nA bandeira é atribuída automaticamente na criação do cartão!",
                "keywords": "bandeira, visa, mastercard, elo",
                "intent": "bandeiras_cartao",
                "variations": [
                    "Que bandeiras tem",
                    "Quais cartões vocês têm",
                    "Bandeiras disponíveis"
                ]
            },
            {
                "category": "cartoes",
                "question": "Como fazer uma compra no cartão?",
                "answer": "Para fazer compra no cartão:\n\nPOST /api/v1/credit-cards/{card_id}/purchase\n\nEnvie:\n{\n  \"amount\": 400.00,\n  \"merchant\": \"Loja XYZ\",\n  \"installments\": 3,\n  \"description\": \"Notebook\"\n}\n\nVocê pode parcelar em até 24x!",
                "keywords": "comprar, compra, cartao, parcelar",
                "intent": "comprar_cartao",
                "variations": [
                    "Quero comprar no cartão",
                    "Como uso o cartão",
                    "Fazer compra parcelada"
                ]
            },
            {
                "category": "cartoes",
                "question": "Como pagar a fatura do cartão?",
                "answer": "Para pagar fatura do cartão:\n\nPOST /api/v1/credit-cards/{card_id}/pay-bill\n\nEnvie:\n{\n  \"account_id\": 123,\n  \"amount\": 500.00\n}\n\nPode pagar parcial ou total. O valor é debitado da sua conta na hora!",
                "keywords": "fatura, pagar fatura, cartao",
                "intent": "pagar_fatura",
                "variations": [
                    "Quero pagar a fatura",
                    "Como pago o cartão",
                    "Pagar fatura do crédito"
                ]
            },
            
            # ===== CATEGORIA: INVESTIMENTOS =====
            {
                "category": "investimentos",
                "question": "Quais investimentos estão disponíveis?",
                "answer": "Temos 11 ativos disponíveis:\n\n**Ações (9):**\n• NEXG - NexGen Innovations (Tecnologia)\n• AETH - AetherNet Solutions (Tecnologia)\n• QTXD - Quantex Data (Tecnologia)\n• URBP - UrbanPulse Retail (Varejo)\n• FLSH - Flourish Foods (Varejo)\n• TNVM - TerraNova Mining (Energia)\n• VLTX - Voltix Energy (Energia)\n• INSC - Insight Capital (Finanças)\n• MDCR - MediCare Solutions (Saúde)\n\n**Fundos (2):**\n• APXRF - Apex RF Simples\n• APXRFP - Apex RF Performance\n\nVeja todos em: GET /api/v1/investments/assets",
                "keywords": "investir, investimento, acoes, fundos",
                "intent": "listar_investimentos",
                "variations": [
                    "O que posso investir",
                    "Quais ações tem",
                    "Investimentos disponíveis"
                ]
            },
            {
                "category": "investimentos",
                "question": "Como comprar uma ação?",
                "answer": "Para comprar ações:\n\n1. Você precisa ter uma **Conta Investimento**\n2. Faça POST para /api/v1/investments/buy\n\nEnvie:\n{\n  \"account_id\": 123,\n  \"asset_id\": 1,\n  \"quantity\": 10\n}\n\nO valor é calculado automaticamente pelo preço atual!",
                "keywords": "comprar, acao, investir",
                "intent": "comprar_acao",
                "variations": [
                    "Quero comprar ações",
                    "Como invisto",
                    "Comprar investimento"
                ]
            },
            {
                "category": "investimentos",
                "question": "Como vender uma ação?",
                "answer": "Para vender ações:\n\nPOST /api/v1/investments/sell\n\nEnvie:\n{\n  \"account_id\": 123,\n  \"asset_id\": 1,\n  \"quantity\": 5\n}\n\nO lucro/prejuízo é calculado automaticamente e creditado na sua conta!",
                "keywords": "vender, acao, lucro",
                "intent": "vender_acao",
                "variations": [
                    "Quero vender ações",
                    "Como faço venda",
                    "Vender investimento"
                ]
            },
            {
                "category": "investimentos",
                "question": "Como ver meu portfólio?",
                "answer": "Para ver seu portfólio:\n\nGET /api/v1/investments/portfolio?account_id=123\n\nOu para resumo consolidado:\nGET /api/v1/investments/portfolio/summary?account_id=123\n\nVocê verá:\n• Ativos que possui\n• Quantidade de cada\n• Preço médio de compra\n• Valor atual\n• Lucro/Prejuízo",
                "keywords": "portfolio, carteira, investimentos",
                "intent": "ver_portfolio",
                "variations": [
                    "Ver meus investimentos",
                    "Mostrar carteira",
                    "Meu portfólio"
                ]
            },
            {
                "category": "investimentos",
                "question": "Os preços são atualizados em tempo real?",
                "answer": "Sim! Temos um **simulador de mercado em tempo real**!\n\n• Preços atualizam a cada 10 segundos\n• Volatilidade realista (Ações ±2%, Fundos ±0.5%)\n• Você pode acompanhar via **WebSocket**\n\nConecte-se:\nws://localhost:8000/ws/market-feed\n\nReceba atualizações instantâneas de preços!",
                "keywords": "tempo real, preco, atualizar, websocket",
                "intent": "preco_tempo_real",
                "variations": [
                    "Preços atualizam",
                    "Tempo real",
                    "Cotação ao vivo"
                ]
            },
            
            # ===== CATEGORIA: SEGURANÇA =====
            {
                "category": "seguranca",
                "question": "Como faço login?",
                "answer": "Você pode fazer login de 3 formas:\n\nPOST /api/v1/auth/login\n\n1. **Por Email:**\n   {\"identifier\": \"email@example.com\", \"password\": \"senha\"}\n\n2. **Por CPF:**\n   {\"identifier\": \"123.456.789-10\", \"password\": \"senha\"}\n\n3. **Por Número da Conta:**\n   {\"identifier\": \"12345-6\", \"password\": \"senha\"}\n\nVocê receberá um token JWT para usar nas próximas requisições!",
                "keywords": "login, entrar, senha",
                "intent": "fazer_login",
                "variations": [
                    "Como entro",
                    "Fazer login",
                    "Acessar conta"
                ]
            },
            {
                "category": "seguranca",
                "question": "Meus dados estão seguros?",
                "answer": "Sim! Temos várias camadas de segurança:\n\n• **Senhas** são criptografadas com bcrypt\n• **Tokens JWT** com expiração de 30 minutos\n• **Validação** em todas as operações\n• **Proteção de rotas** - só você acessa suas informações\n• **Transações atômicas** - rollback automático em falhas\n• **HTTPS** recomendado para produção\n\nSeus dados estão protegidos!",
                "keywords": "seguranca, seguro, protecao",
                "intent": "info_seguranca",
                "variations": [
                    "É seguro",
                    "Proteção de dados",
                    "Segurança do banco"
                ]
            },
            
            # ===== CATEGORIA: SUPORTE =====
            {
                "category": "suporte",
                "question": "Como entro em contato com o suporte?",
                "answer": "Você pode:\n\n1. **Usar este chatbot** - Estou aqui para ajudar 24/7!\n2. **Email:** suporte@digitalbank.com\n3. **Telefone:** (11) 4000-0000\n4. **WhatsApp:** (11) 99999-9999\n\nEstamos sempre prontos para te ajudar!",
                "keywords": "suporte, ajuda, contato, telefone",
                "intent": "contato_suporte",
                "variations": [
                    "Falar com suporte",
                    "Preciso de ajuda",
                    "Contato do banco"
                ]
            },
            {
                "category": "suporte",
                "question": "Onde vejo a documentação da API?",
                "answer": "Temos documentação completa!\n\n• **Swagger UI:** http://localhost:8000/docs\n• **ReDoc:** http://localhost:8000/redoc\n• **GitHub:** (link do repositório)\n\nLá você encontra:\n• Todos os endpoints\n• Exemplos de requisições\n• Schemas de dados\n• Como testar",
                "keywords": "documentacao, api, swagger, docs",
                "intent": "ver_documentacao",
                "variations": [
                    "Documentação da API",
                    "Onde está os docs",
                    "Ver API docs"
                ]
            },
            {
                "category": "suporte",
                "question": "Qual o horário de atendimento?",
                "answer": "**Digital Superbank funciona 24/7!**\n\n• API disponível 24 horas\n• PIX 24/7\n• Chatbot sempre ativo\n• Transações a qualquer hora\n\nAtendimento humano:\n• Segunda a Sexta: 8h às 20h\n• Sábado: 8h às 14h\n• Domingo e feriados: Chatbot",
                "keywords": "horario, atendimento, funcionamento",
                "intent": "horario_atendimento",
                "variations": [
                    "Que horas funciona",
                    "Horário do banco",
                    "Quando posso usar"
                ]
            },
            
            # ===== CATEGORIA: GERAL =====
            {
                "category": "geral",
                "question": "O que é o Digital Superbank?",
                "answer": "**Digital Superbank** é um sistema bancário digital completo!\n\nOferecemos:\n• 7 tipos de contas\n• Transações (PIX, boletos, transferências)\n• Cartões de crédito (3 categorias)\n• Investimentos (11 ativos)\n• Simulador de mercado em tempo real\n• WebSocket para dados ao vivo\n• API REST completa\n• Chatbot inteligente (eu!)\n\nTudo 100% digital e seguro!",
                "keywords": "digital superbank, banco, o que e",
                "intent": "info_banco",
                "variations": [
                    "O que é isso",
                    "Sobre o banco",
                    "Quem é Digital Superbank"
                ]
            },
            {
                "category": "geral",
                "question": "Obrigado!",
                "answer": "Por nada! 😊\n\nFico feliz em ajudar! Se precisar de mais alguma coisa, é só perguntar.\n\nLembre-se: estou aqui 24/7 para te ajudar com:\n• Contas\n• Transações\n• Cartões\n• Investimentos\n• E muito mais!\n\nTenha um ótimo dia!",
                "keywords": "obrigado, obrigada, valeu",
                "intent": "agradecimento",
                "variations": [
                    "Valeu",
                    "Muito obrigado",
                    "Brigadão"
                ]
            },
        ]
        
        print("📊 Populando base de conhecimento...")
        print()
        
        for idx, item_data in enumerate(knowledge_items, 1):
            variations = item_data.pop('variations', [])
            
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
            
            print(f"✅ [{idx}/{len(knowledge_items)}] {item_data['category']}: {item_data['question'][:50]}...")
        
        db.commit()
        
        print()
        print("=" * 80)
        print("✅ BASE DE CONHECIMENTO POPULADA COM SUCESSO!")
        print("=" * 80)
        print(f"📊 Total de itens: {len(knowledge_items)}")
        print()
        print("📚 Categorias criadas:")
        categories = db.query(KnowledgeBase.category).distinct().all()
        for cat in categories:
            count = db.query(KnowledgeBase).filter(
                KnowledgeBase.category == cat[0]
            ).count()
            print(f"   • {cat[0].capitalize()}: {count} itens")
        print()
        print("🤖 O chatbot está pronto para uso!")
        print("   Endpoint: POST /api/v1/chatbot/message")
        print()
        
    except Exception as e:
        print(f"❌ Erro ao popular base de conhecimento: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    populate_knowledge_base()
