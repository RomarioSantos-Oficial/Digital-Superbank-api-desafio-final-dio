import React, { useState, useEffect, useRef, useContext } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import { 
  IoChatbubbles, IoClose, IoSend, IoRefresh, 
  IoChevronDown, IoChevronUp, IoThumbsUp, IoThumbsDown 
} from 'react-icons/io5';
import toast from 'react-hot-toast';
import { AuthContext } from '../../context/AuthContext';
import * as chatbotService from '../../services/chatbot.service';
import * as accountService from '../../services/account.service';
import * as investmentService from '../../services/investment.service';

const FloatingChatbot = () => {
  const { user, isAuthenticated } = useContext(AuthContext);
  const navigate = useNavigate();
  
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [messages, setMessages] = useState(() => {
    // Recupera mensagens do localStorage ao iniciar
    const saved = localStorage.getItem('luna_messages');
    return saved ? JSON.parse(saved) : [];
  });
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [sessionId, setSessionId] = useState(() => {
    // Recupera sessionId do localStorage ao iniciar
    return localStorage.getItem('luna_session_id') || null;
  });
  const [suggestions, setSuggestions] = useState(() => {
    // Recupera sugestões do localStorage
    const saved = localStorage.getItem('luna_suggestions');
    return saved ? JSON.parse(saved) : [];
  });
  const [userAccounts, setUserAccounts] = useState([]);
  const [userPortfolio, setUserPortfolio] = useState(null);
  const messagesEndRef = useRef(null);
  const hasLoadedHistory = useRef(false);
  
  // Salva sessionId no localStorage quando mudar
  useEffect(() => {
    if (sessionId) {
      localStorage.setItem('luna_session_id', sessionId);
    }
  }, [sessionId]);
  
  // Salva mensagens no localStorage quando mudarem
  useEffect(() => {
    if (messages.length > 0) {
      localStorage.setItem('luna_messages', JSON.stringify(messages));
    }
  }, [messages]);
  
  // Salva sugestões no localStorage quando mudarem
  useEffect(() => {
    if (suggestions.length > 0) {
      localStorage.setItem('luna_suggestions', JSON.stringify(suggestions));
    }
  }, [suggestions]);
  
  // Verifica se usuário está logado
  useEffect(() => {
    if (isOpen && !isAuthenticated()) {
      toast.error('Você precisa estar logado para usar a Luna!');
      setIsOpen(false);
    }
  }, [isOpen, isAuthenticated]);

  // Inicializa o chat ao abrir pela primeira vez (APENAS UMA VEZ)
  useEffect(() => {
    if (isOpen && isAuthenticated() && !hasLoadedHistory.current) {
      initializeChat();
      loadUserData();
      hasLoadedHistory.current = true;
    }
  }, [isOpen]); // Remove outras dependências que causam re-render

  const loadUserData = async () => {
    try {
      // Carregar contas do usuário
      const accounts = await accountService.getAccounts();
      setUserAccounts(accounts);
      
      // Carregar portfólio se tiver conta de investimento
      if (accounts && accounts.length > 0) {
        // Busca conta de investimento
        const investmentAccount = accounts.find(
          acc => acc.account_type === 'INVESTIMENTO'
        );
        
        if (investmentAccount) {
          const portfolio = await investmentService.getPortfolioSummary(investmentAccount.id);
          setUserPortfolio(portfolio);
        }
      }
    } catch (error) {
      console.error('Erro ao carregar dados do usuário:', error);
    }
  };

  const initializeChat = async () => {
    // Se já tem mensagens no localStorage, não precisa carregar do banco
    if (messages.length > 0) {
      hasLoadedHistory.current = true;
      return;
    }
    
    // Se já tem sessionId, tenta carregar histórico do banco
    if (sessionId) {
      try {
        const history = await chatbotService.getChatHistory(sessionId);
        if (history && history.messages && history.messages.length > 0) {
          // Converte mensagens do histórico para o formato do componente
          const loadedMessages = history.messages.map(msg => ({
            id: msg.id,
            text: msg.message,
            sender: msg.is_user ? 'user' : 'bot',
            timestamp: new Date(msg.timestamp),
            confidence: msg.confidence,
            intent: msg.intent,
            messageId: msg.id
          }));
          
          setMessages(loadedMessages);
          hasLoadedHistory.current = true;
          
          // Carrega sugestões
          const popularQuestions = await chatbotService.getPopularQuestions(8);
          setSuggestions(popularQuestions);
          
          return;
        }
      } catch (error) {
        console.error('Erro ao carregar histórico:', error);
        // Se falhou, continua com mensagem de boas-vindas
      }
    }
    
    // Mensagem de boas-vindas personalizada (apenas para nova sessão)
    const welcomeMessage = user?.name 
      ? `Olá, ${user.name}! 👋 Eu sou a Luna, sua assistente virtual. Como posso ajudá-lo hoje?`
      : 'Olá! 👋 Eu sou a Luna, sua assistente virtual do Digital Superbank. Como posso ajudá-lo hoje?';
    
    setMessages([
      {
        id: Date.now(),
        text: welcomeMessage,
        sender: 'bot',
        timestamp: new Date()
      }
    ]);
    
    hasLoadedHistory.current = true;

    // Carregar sugestões
    try {
      const popularQuestions = await chatbotService.getPopularQuestions(8);
      setSuggestions(popularQuestions);
    } catch (error) {
      console.error('Erro ao carregar sugestões:', error);
      setSuggestions([
        'Qual é meu saldo?',
        'Quais são minhas ações?',
        'Pagar contas',
        'Fazer um PIX',
        'Como investir?',
        'Solicitar cartão',
        'Ver extrato',
        'Transferir dinheiro'
      ]);
    }
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const processUserCommand = async (messageText) => {
    const lowerMessage = messageText.toLowerCase();
    
    // Comandos de navegação - detecta pedidos para abrir páginas
    const navigationCommands = {
      'abrir investimentos': '/investments',
      'abra investimentos': '/investments',
      'abre investimentos': '/investments',
      'página de investimentos': '/investments',
      'pagina de investimentos': '/investments',
      'ir para investimentos': '/investments',
      'quero investir': '/investments',
      
      'abrir transações': '/transactions',
      'abra transações': '/transactions',
      'abrir transacoes': '/transactions',
      'página de transações': '/transactions',
      'fazer pix': '/transactions',
      'enviar pix': '/transactions',
      'transferir': '/transactions',
      'transferência': '/transactions',
      'transferencia': '/transactions',
      
      'abrir contas': '/accounts',
      'abra contas': '/accounts',
      'minhas contas': '/accounts',
      'ver contas': '/accounts',
      'página de contas': '/accounts',
      
      'abrir extrato': '/statement',
      'abra extrato': '/statement',
      'ver extrato': '/statement',
      'meu extrato': '/statement',
      'histórico': '/statement',
      'historico': '/statement',
      
      'abrir cartões': '/cards',
      'abra cartões': '/cards',
      'abrir cartoes': '/cards',
      'meus cartões': '/cards',
      'meus cartoes': '/cards',
      'cartão': '/cards',
      'cartao': '/cards',
      
      'abrir perfil': '/profile',
      'abra perfil': '/profile',
      'meu perfil': '/profile',
      'meus dados': '/profile',
      'configurações': '/profile',
      'configuracoes': '/profile',
      
      'abrir pagamentos': '/pay-bills',
      'abra pagamentos': '/pay-bills',
      'pagar conta': '/pay-bills',
      'pagar boleto': '/pay-bills',
      'boleto': '/pay-bills',
      'contas a pagar': '/pay-bills'
    };
    
    // Verifica comandos de navegação primeiro
    for (const [command, route] of Object.entries(navigationCommands)) {
      if (lowerMessage.includes(command)) {
        const pageNames = {
          '/pay-bills': 'pagamentos',
          '/transactions': 'transações',
          '/statement': 'extrato',
          '/investments': 'investimentos',
          '/cards': 'cartões',
          '/profile': 'perfil',
          '/accounts': 'contas'
        };
        
        return {
          response: `Abrindo ${pageNames[route]} para você! ✨`,
          confidence: 1.0,
          intent: 'navegar',
          action: 'navigate',
          navigation: route
        };
      }
    }
    
    // Comandos de saldo
    if (lowerMessage.includes('saldo') || lowerMessage.includes('quanto tenho')) {
      if (userAccounts.length > 0) {
        const account = userAccounts[0];
        return {
          response: `Seu saldo atual é de R$ ${account.balance?.toFixed(2) || '0.00'}. 💰\n\nConta: ${account.account_number}\nTipo: ${account.account_type}`,
          confidence: 1.0,
          intent: 'consultar_saldo'
        };
      }
    }
    
    // Comandos de ações/investimentos
    if (lowerMessage.includes('ações') || lowerMessage.includes('acoes') || lowerMessage.includes('investimentos') || lowerMessage.includes('portfólio') || lowerMessage.includes('portfolio')) {
      if (userPortfolio) {
        const total = userPortfolio.total_value || 0;
        const profit = userPortfolio.total_profit || 0;
        const profitPercent = userPortfolio.profit_percentage || 0;
        
        return {
          response: `📊 Seu portfólio:\n\nValor Total: R$ ${total.toFixed(2)}\nLucro: R$ ${profit.toFixed(2)} (${profitPercent.toFixed(2)}%)\n\nDeseja ver mais detalhes? Posso abrir a página de investimentos para você!`,
          confidence: 1.0,
          intent: 'consultar_investimentos',
          action: 'offer_navigation',
          navigation: '/investments'
        };
      }
    }
    
    // Comandos de preço de ações
    if (lowerMessage.includes('preço') && (lowerMessage.includes('ação') || lowerMessage.includes('acao'))) {
      return {
        response: 'Para consultar preços de ações em tempo real, vou abrir a página de investimentos para você! 📈',
        confidence: 1.0,
        intent: 'consultar_preco',
        action: 'navigate',
        navigation: '/investments'
      };
    }
    
    return null;
  };

  const sendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    const messageText = inputMessage;
    setInputMessage('');
    setIsTyping(true);

    try {
      // Primeiro tenta processar comandos personalizados
      const customResponse = await processUserCommand(messageText);
      
      if (customResponse) {
        // Simula digitação - espera 3 segundos
        await new Promise(resolve => setTimeout(resolve, 3000));
        
        const botMessage = {
          id: Date.now() + 1,
          text: customResponse.response,
          sender: 'bot',
          timestamp: new Date(),
          confidence: customResponse.confidence,
          intent: customResponse.intent,
          action: customResponse.action,
          navigation: customResponse.navigation
        };

        setMessages(prev => [...prev, botMessage]);
        setIsTyping(false);
        
        // Navegar se necessário
        if (customResponse.action === 'navigate' && customResponse.navigation) {
          setTimeout(() => {
            navigate(customResponse.navigation);
            setIsMinimized(true);
          }, 1500);
        }
        
        return;
      }
      
      // Se não for comando personalizado, usa a API do chatbot
      // Simula digitação - espera 3 segundos
      await new Promise(resolve => setTimeout(resolve, 3000));
      
      const response = await chatbotService.sendMessage(messageText, sessionId);

      const botMessage = {
        id: Date.now() + 1,
        text: response.response,
        sender: 'bot',
        timestamp: new Date(),
        confidence: response.confidence,
        intent: response.intent,
        messageId: response.message_id
      };

      setMessages(prev => [...prev, botMessage]);
      
      // Atualizar session_id
      if (response.session_id) {
        setSessionId(response.session_id);
      }

      // Atualizar sugestões se houver
      if (response.suggestions && response.suggestions.length > 0) {
        setSuggestions(response.suggestions);
      }
    } catch (error) {
      console.error('Erro no chatbot:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Desculpe, ocorreu um erro. Tente novamente ou reformule sua pergunta.',
        sender: 'bot',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      toast.error('Erro ao comunicar com o chatbot');
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const resetConversation = () => {
    setMessages([]);
    setSessionId(null);
    setSuggestions([]);
    hasLoadedHistory.current = false;
    // Limpa todos os dados do localStorage
    localStorage.removeItem('luna_session_id');
    localStorage.removeItem('luna_messages');
    localStorage.removeItem('luna_suggestions');
    loadUserData();
    initializeChat();
    toast.success('Conversa reiniciada');
  };

  const handleFeedback = async (messageId, isHelpful) => {
    try {
      await chatbotService.submitFeedback(messageId, isHelpful);
      toast.success(isHelpful ? 'Obrigado pelo feedback!' : 'Agradecemos seu feedback');
    } catch (error) {
      console.error('Erro ao enviar feedback:', error);
    }
  };

  const formatTime = (date) => {
    return new Date(date).toLocaleTimeString('pt-BR', {
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleQuickQuestion = (question) => {
    setInputMessage(question);
    setTimeout(() => sendMessage(), 100);
  };

  return (
    <>
      {/* Floating Button */}
      <AnimatePresence>
        {!isOpen && isAuthenticated() && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsOpen(true)}
            className="fixed bottom-6 left-6 z-50 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-full shadow-2xl hover:shadow-blue-500/50 transition-all overflow-hidden"
          >
            <div className="relative p-2">
              <img 
                src="/luna.png" 
                alt="Luna" 
                className="w-16 h-16 rounded-full object-cover border-2 border-white"
                onError={(e) => {
                  e.target.style.display = 'none';
                  e.target.nextSibling.style.display = 'block';
                }}
              />
              <IoChatbubbles className="w-16 h-16 hidden" />
              <motion.span
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ repeat: Infinity, duration: 2 }}
                className="absolute -top-1 -right-1 bg-green-400 text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center shadow-lg"
              >
                ✨
              </motion.span>
            </div>
          </motion.button>
        )}
      </AnimatePresence>

      {/* Chat Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 100, scale: 0.8 }}
            animate={{ 
              opacity: 1, 
              y: 0, 
              scale: 1
            }}
            exit={{ opacity: 0, y: 100, scale: 0.8 }}
            transition={{ type: 'spring', damping: 25, stiffness: 300 }}
            className={`fixed bottom-6 left-6 z-50 w-96 bg-gray-800 rounded-2xl shadow-2xl border border-gray-700 flex flex-col ${isMinimized ? 'h-auto' : 'h-[600px]'}`}
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-500 to-purple-600 p-4 flex items-center justify-between flex-shrink-0">
              <div className="flex items-center gap-3">
                <div className="relative">
                  <img 
                    src="/luna.png" 
                    alt="Luna" 
                    className="w-10 h-10 rounded-full object-cover border-2 border-white"
                    onError={(e) => {
                      e.target.style.display = 'none';
                      e.target.nextSibling.style.display = 'block';
                    }}
                  />
                  <IoChatbubbles className="w-10 h-10 text-white hidden" />
                  <span className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-400 rounded-full border-2 border-blue-600"></span>
                </div>
                <div>
                  <h3 className="text-white font-bold">Luna</h3>
                  <p className="text-xs text-blue-100">Assistente Virtual • Online</p>
                </div>
              </div>
              <div className="flex items-center gap-1">
                <button
                  onClick={() => setIsMinimized(!isMinimized)}
                  className="text-white hover:bg-white hover:bg-opacity-30 p-2 rounded-lg transition-all"
                  title={isMinimized ? 'Maximizar' : 'Minimizar'}
                >
                  {isMinimized ? <IoChevronUp className="w-5 h-5" /> : <IoChevronDown className="w-5 h-5" />}
                </button>
                <button
                  onClick={resetConversation}
                  className="text-white hover:bg-white hover:bg-opacity-30 p-2 rounded-lg transition-all"
                  title="Reiniciar conversa"
                >
                  <IoRefresh className="w-5 h-5" />
                </button>
                <button
                  onClick={() => setIsOpen(false)}
                  className="text-white hover:bg-red-500 hover:bg-opacity-50 p-2 rounded-lg transition-all"
                  title="Fechar"
                >
                  <IoClose className="w-6 h-6" />
                </button>
              </div>
            </div>

            {/* Chat Body */}
            {!isMinimized && (
              <div className="flex-1 flex flex-col overflow-hidden">
                <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-900">
                  {messages.map((message) => (
                    <motion.div
                      key={message.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className={`flex gap-2 ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      {/* Avatar da Luna para mensagens do bot */}
                      {message.sender === 'bot' && (
                        <img 
                          src="/luna.png" 
                          alt="Luna" 
                          className="w-8 h-8 rounded-full object-cover border-2 border-blue-500 flex-shrink-0"
                          onError={(e) => {
                            e.target.style.display = 'none';
                          }}
                        />
                      )}
                      
                      <div className="max-w-[80%]">
                        <div
                          className={`rounded-2xl p-3 ${
                            message.sender === 'user'
                              ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                              : 'bg-gray-700 text-white'
                          }`}
                        >
                          <p className="text-sm whitespace-pre-wrap">{message.text}</p>
                          <div className="flex items-center justify-between mt-2">
                            <p className="text-xs opacity-70">
                              {formatTime(message.timestamp)}
                            </p>
                            {message.confidence && (
                              <p className="text-xs opacity-70">
                                {(message.confidence * 100).toFixed(0)}%
                              </p>
                            )}
                          </div>
                          {message.intent && (
                            <p className="text-xs opacity-50 mt-1 italic">
                              {message.intent}
                            </p>
                          )}
                        </div>
                        
                        {/* Feedback buttons for bot messages */}
                        {message.sender === 'bot' && message.messageId && (
                          <div className="flex gap-2 mt-2 ml-2">
                            <button
                              onClick={() => handleFeedback(message.messageId, true)}
                              className="text-xs text-gray-400 hover:text-green-400 transition-colors flex items-center gap-1"
                              title="Resposta útil"
                            >
                              <IoThumbsUp className="w-3 h-3" />
                            </button>
                            <button
                              onClick={() => handleFeedback(message.messageId, false)}
                              className="text-xs text-gray-400 hover:text-red-400 transition-colors flex items-center gap-1"
                              title="Resposta não útil"
                            >
                              <IoThumbsDown className="w-3 h-3" />
                            </button>
                          </div>
                        )}
                      </div>
                    </motion.div>
                  ))}

                  {isTyping && (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="flex gap-2 justify-start items-end"
                    >
                      <img 
                        src="/luna.png" 
                        alt="Luna" 
                        className="w-8 h-8 rounded-full object-cover border-2 border-blue-500 flex-shrink-0"
                        onError={(e) => {
                          e.target.style.display = 'none';
                        }}
                      />
                      <div className="bg-gray-700 rounded-2xl p-3">
                        <div className="flex space-x-2">
                          <motion.div
                            animate={{ y: [0, -10, 0] }}
                            transition={{ repeat: Infinity, duration: 0.6, delay: 0 }}
                            className="w-2 h-2 bg-blue-400 rounded-full"
                          />
                          <motion.div
                            animate={{ y: [0, -10, 0] }}
                            transition={{ repeat: Infinity, duration: 0.6, delay: 0.2 }}
                            className="w-2 h-2 bg-purple-400 rounded-full"
                          />
                          <motion.div
                            animate={{ y: [0, -10, 0] }}
                            transition={{ repeat: Infinity, duration: 0.6, delay: 0.4 }}
                            className="w-2 h-2 bg-pink-400 rounded-full"
                          />
                        </div>
                      </div>
                    </motion.div>
                  )}

                  <div ref={messagesEndRef} />
                </div>

                {/* Quick Questions */}
                {suggestions.length > 0 && (
                  <div className="p-4 bg-gray-800 border-t border-gray-700 flex-shrink-0">
                    <p className="text-xs text-gray-400 mb-2">
                      {messages.length === 1 ? 'Perguntas frequentes:' : 'Você também pode perguntar:'}
                    </p>
                    <div className="grid grid-cols-2 gap-2">
                      {suggestions.slice(0, 4).map((question, index) => (
                        <button
                          key={index}
                          onClick={() => handleQuickQuestion(question)}
                          className="text-xs bg-gray-700 hover:bg-gray-600 text-white p-2 rounded-lg transition-all text-left"
                        >
                          {question}
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {/* Input */}
                <div className="p-4 bg-gray-800 border-t border-gray-700 flex-shrink-0">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={inputMessage}
                      onChange={(e) => setInputMessage(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Digite sua mensagem..."
                      className="flex-1 bg-gray-700 text-white px-4 py-2 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <button
                      onClick={sendMessage}
                      disabled={!inputMessage.trim() || isTyping}
                      className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-2 rounded-xl hover:shadow-lg transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <IoSend className="w-6 h-6" />
                    </button>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
};

export default FloatingChatbot;
