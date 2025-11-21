"""
Script de teste do Chatbot
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Cores para output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'


def print_response(response_data):
    """Imprime resposta formatada do bot"""
    print(f"\n{CYAN}🤖 BOT:{RESET} {response_data['response']}")
    if response_data.get('intent'):
        print(f"{YELLOW}   └─ Intenção: {response_data['intent']} (confiança: {response_data['confidence']}){RESET}")
    if response_data.get('suggestions'):
        print(f"{BLUE}   └─ Sugestões:{RESET}")
        for sug in response_data['suggestions']:
            print(f"      • {sug}")


def test_chatbot():
    """Testa o chatbot com várias perguntas"""
    print("=" * 80)
    print(f"{GREEN}🤖 TESTE DO CHATBOT - DIGITAL SUPERBANK{RESET}")
    print("=" * 80)
    print()
    
    # Lista de perguntas para testar
    questions = [
        "Olá!",
        "Como abrir uma conta?",
        "Quais tipos de contas existem?",
        "Qual o limite de saque?",
        "Como fazer PIX?",
        "Quero solicitar um cartão de crédito",
        "Quais investimentos estão disponíveis?",
        "Como comprar ações?",
        "Os preços são atualizados em tempo real?",
        "É seguro?",
        "Obrigado!",
    ]
    
    session_id = None
    
    for idx, question in enumerate(questions, 1):
        print(f"\n{'-' * 80}")
        print(f"{BLUE}👤 VOCÊ:{RESET} {question}")
        
        # Envia mensagem
        data = {"message": question}
        if session_id:
            data["session_id"] = session_id
        
        try:
            response = requests.post(
                f"{BASE_URL}/chatbot/message",
                json=data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                session_id = result['session_id']  # Mantém sessão
                print_response(result)
            else:
                print(f"{RED}❌ Erro: {response.status_code}{RESET}")
                print(response.text)
        
        except Exception as e:
            print(f"{RED}❌ Erro na requisição: {e}{RESET}")
    
    print(f"\n{'-' * 80}")
    print()
    
    # Teste de histórico
    if session_id:
        print(f"{YELLOW}📊 TESTANDO HISTÓRICO DA CONVERSA...{RESET}")
        try:
            response = requests.get(
                f"{BASE_URL}/chatbot/history/{session_id}",
                timeout=10
            )
            
            if response.status_code == 200:
                history = response.json()
                print(f"{GREEN}✅ Histórico recuperado!{RESET}")
                print(f"   Total de mensagens: {len(history['messages'])}")
                print(f"   Início: {history['started_at']}")
            else:
                print(f"{RED}❌ Erro ao buscar histórico{RESET}")
        except Exception as e:
            print(f"{RED}❌ Erro: {e}{RESET}")
    
    print()
    
    # Teste de estatísticas
    print(f"{YELLOW}📈 TESTANDO ESTATÍSTICAS...{RESET}")
    try:
        response = requests.get(f"{BASE_URL}/chatbot/stats", timeout=10)
        
        if response.status_code == 200:
            stats = response.json()
            print(f"{GREEN}✅ Estatísticas:{RESET}")
            print(f"   Conversas: {stats['total_conversations']}")
            print(f"   Mensagens: {stats['total_messages']}")
            print(f"   Confiança média: {stats['average_confidence']}")
            print(f"   Intenções mais usadas:")
            for intent_data in stats['most_used_intents'][:5]:
                print(f"      • {intent_data['intent']}: {intent_data['count']}x")
        else:
            print(f"{RED}❌ Erro ao buscar estatísticas{RESET}")
    except Exception as e:
        print(f"{RED}❌ Erro: {e}{RESET}")
    
    print()
    
    # Teste de sugestões
    print(f"{YELLOW}💡 TESTANDO SUGESTÕES POPULARES...{RESET}")
    try:
        response = requests.get(f"{BASE_URL}/chatbot/suggestions?limit=5", timeout=10)
        
        if response.status_code == 200:
            suggestions = response.json()
            print(f"{GREEN}✅ Perguntas populares:{RESET}")
            for sug in suggestions:
                print(f"   • {sug}")
        else:
            print(f"{RED}❌ Erro ao buscar sugestões{RESET}")
    except Exception as e:
        print(f"{RED}❌ Erro: {e}{RESET}")
    
    print()
    print("=" * 80)
    print(f"{GREEN}✅ TESTE DO CHATBOT CONCLUÍDO!{RESET}")
    print("=" * 80)
    print()
    print(f"{BLUE}💡 Dicas:{RESET}")
    print("   • O chatbot funciona sem autenticação")
    print("   • Mantém histórico de conversas por sessão")
    print("   • Detecta intenções automaticamente")
    print("   • Aprende com feedback dos usuários")
    print("   • Suporta variações de perguntas")
    print()


if __name__ == "__main__":
    try:
        test_chatbot()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}⛔ Teste interrompido pelo usuário{RESET}")
    except Exception as e:
        print(f"\n\n{RED}❌ Erro durante teste: {e}{RESET}")
