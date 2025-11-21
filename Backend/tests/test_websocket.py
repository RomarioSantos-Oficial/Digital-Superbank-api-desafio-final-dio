"""
Teste de WebSocket - Streaming de Preços em Tempo Real
"""
import asyncio
import websockets
import json

WEBSOCKET_URL = "ws://localhost:8000/ws/market-feed"


async def test_websocket():
    """Testa conexão WebSocket e recebe atualizações de preços"""
    print("="  * 80)
    print("🔌 TESTE DE WEBSOCKET - STREAMING DE PREÇOS EM TEMPO REAL")
    print("=" * 80)
    print()
    print(f"Conectando a: {WEBSOCKET_URL}")
    print("Pressione Ctrl+C para encerrar")
    print()
    
    try:
        async with websockets.connect(WEBSOCKET_URL) as websocket:
            print("✅ Conectado ao WebSocket!")
            print()
            
            message_count = 0
            
            while True:
                try:
                    # Recebe mensagem do servidor
                    message = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(message)
                    
                    message_count += 1
                    
                    # Exibe conforme o tipo de mensagem
                    if data.get("type") == "connected":
                        print(f"📡 {data['message']}")
                        print(f"   Ativos disponíveis: {data['assets_count']}")
                        print()
                    
                    elif data.get("type") == "price_update":
                        # Exibe update de preço
                        symbol = data.get("symbol", "???")
                        name = data.get("name", "")
                        price = data.get("price", 0.0)
                        timestamp = data.get("timestamp", "")
                        
                        print(f"📊 [{timestamp[:19]}] {symbol:6s} - {name:30s} | R$ {price:8.2f}")
                        
                        # A cada 20 mensagens, mostra resumo
                        if message_count % 20 == 0:
                            print()
                            print(f"   📈 {message_count} atualizações recebidas...")
                            print()
                
                except asyncio.TimeoutError:
                    print("⏳ Aguardando atualizações...")
                except json.JSONDecodeError:
                    print("⚠️  Mensagem inválida recebida")
                
    except websockets.exceptions.ConnectionClosed:
        print()
        print("🔌 Conexão WebSocket encerrada pelo servidor")
    except ConnectionRefusedError:
        print()
        print("❌ Erro: Não foi possível conectar ao WebSocket")
        print("   Certifique-se de que a API está rodando:")
        print("   uvicorn main:app --reload")
    except KeyboardInterrupt:
        print()
        print()
        print("⛔ Teste interrompido pelo usuário")
    except Exception as e:
        print()
        print(f"❌ Erro inesperado: {e}")


def main():
    """Função principal"""
    asyncio.run(test_websocket())


if __name__ == "__main__":
    main()
