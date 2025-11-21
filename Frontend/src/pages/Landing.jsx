import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  CreditCard,
  TrendingUp,
  Shield,
  Smartphone,
  Zap,
  Globe,
  ArrowRight,
  Check,
  Star,
  Users,
  DollarSign,
  Lock,
  ChevronRight
} from 'lucide-react';
import Button from '../components/common/Button';

const Landing = () => {
  const navigate = useNavigate();
  const [activeFeature, setActiveFeature] = useState(0);

  const features = [
    {
      icon: <CreditCard className="w-8 h-8" />,
      title: 'Cartões Inteligentes',
      description: 'Cartões de crédito com cashback e controle total pelo app',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: 'Investimentos Simplificados',
      description: 'Invista em ações, fundos e renda fixa com apenas alguns cliques',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Transferências Instantâneas',
      description: 'PIX, TED e transferências sem complicação, 24/7',
      color: 'from-yellow-500 to-orange-500'
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'Segurança Máxima',
      description: 'Proteção de ponta a ponta com autenticação biométrica',
      color: 'from-purple-500 to-pink-500'
    }
  ];

  const benefits = [
    { icon: <DollarSign />, text: 'Conta digital 100% gratuita' },
    { icon: <Lock />, text: 'Segurança bancária de nível mundial' },
    { icon: <Smartphone />, text: 'App intuitivo e fácil de usar' },
    { icon: <Globe />, text: 'Atendimento 24/7' },
    { icon: <Star />, text: 'Cashback em todas as compras' },
    { icon: <Users />, text: 'Mais de 1 milhão de clientes' }
  ];

  const testimonials = [
    {
      name: 'Maria Silva',
      role: 'Empreendedora',
      comment: 'O melhor banco digital que já usei. Simples, rápido e sem taxas abusivas!',
      rating: 5
    },
    {
      name: 'João Santos',
      role: 'Desenvolvedor',
      comment: 'Investir nunca foi tão fácil. Interface incrível e suporte excelente.',
      rating: 5
    },
    {
      name: 'Ana Costa',
      role: 'Designer',
      comment: 'Mudei para o Digital Superbank e não me arrependo. Tudo funciona perfeitamente!',
      rating: 5
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % features.length);
    }, 4000);

    return () => clearInterval(interval);
  }, [features.length]);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5
      }
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-gray-900/80 backdrop-blur-lg border-b border-white/10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-3"
            >
              <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-yellow-600 rounded-xl flex items-center justify-center">
                <span className="text-gray-900 font-bold text-xl">D</span>
              </div>
              <span className="text-white font-bold text-xl">Digital Superbank</span>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              className="flex items-center gap-4"
            >
              <Button
                variant="ghost"
                onClick={() => navigate('/login')}
                className="text-white hover:text-yellow-400"
              >
                Entrar
              </Button>
              <Button
                variant="primary"
                onClick={() => navigate('/register')}
                className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold"
              >
                Abrir Conta
              </Button>
            </motion.div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="container mx-auto">
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="text-center max-w-4xl mx-auto"
          >
            <motion.div variants={itemVariants} className="mb-6">
              <span className="inline-block px-4 py-2 bg-yellow-500/20 text-yellow-400 rounded-full text-sm font-semibold mb-6">
                🚀 O futuro do banking já chegou
              </span>
            </motion.div>

            <motion.h1
              variants={itemVariants}
              className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight"
            >
              Seu dinheiro,
              <br />
              <span className="bg-gradient-to-r from-yellow-400 via-yellow-500 to-yellow-600 bg-clip-text text-transparent">
                suas regras
              </span>
            </motion.h1>

            <motion.p
              variants={itemVariants}
              className="text-xl text-gray-200 mb-12 max-w-2xl mx-auto"
            >
              Conta digital completa, investimentos inteligentes e cartões sem anuidade.
              Tudo isso com a segurança que você merece.
            </motion.p>

            <motion.div
              variants={itemVariants}
              className="flex flex-col sm:flex-row items-center justify-center gap-4"
            >
              <Button
                size="lg"
                variant="primary"
                onClick={() => navigate('/register')}
                className="bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold group"
              >
                Abrir Conta Grátis
                <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button
                size="lg"
                variant="outline"
                onClick={() => navigate('/login')}
                className="border-white/20 text-white hover:bg-white/10"
              >
                Já sou cliente
              </Button>
            </motion.div>

            {/* Stats */}
            <motion.div
              variants={itemVariants}
              className="grid grid-cols-3 gap-8 mt-16 max-w-2xl mx-auto"
            >
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">1M+</div>
                <div className="text-gray-400 text-sm">Clientes ativos</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">R$ 5B</div>
                <div className="text-gray-400 text-sm">Transacionados</div>
              </div>
              <div className="text-center">
                <div className="text-3xl font-bold text-white mb-2">4.9★</div>
                <div className="text-gray-400 text-sm">Avaliação</div>
              </div>
            </motion.div>
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-white/5 backdrop-blur-sm">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              Tudo que você precisa em um só lugar
            </h2>
            <p className="text-gray-200 text-lg">
              Recursos completos para você ter controle total das suas finanças
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05, y: -5 }}
                className={`p-6 rounded-2xl bg-gradient-to-br ${feature.color} bg-opacity-10 backdrop-blur-lg border border-white/10 cursor-pointer transition-all ${
                  activeFeature === index ? 'ring-2 ring-yellow-400' : ''
                }`}
                onClick={() => setActiveFeature(index)}
              >
                <div className="w-16 h-16 bg-white/10 rounded-xl flex items-center justify-center mb-4 text-white">
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-200">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-6xl">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-4xl font-bold text-white mb-6">
                Por que escolher o Digital Superbank?
              </h2>
              <p className="text-gray-200 text-lg mb-8">
                Mais de 1 milhão de pessoas já confiam no Digital Superbank para gerenciar
                suas finanças. Junte-se a nós!
              </p>

              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: true }}
                    transition={{ delay: index * 0.1 }}
                    className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors"
                  >
                    <div className="w-10 h-10 bg-yellow-500/20 rounded-lg flex items-center justify-center text-yellow-400">
                      {benefit.icon}
                    </div>
                    <span className="text-white font-medium">{benefit.text}</span>
                    <Check className="w-5 h-5 text-yellow-400 ml-auto" />
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="relative z-10 bg-gradient-to-br from-gray-700 to-gray-900 rounded-3xl p-8 border border-white/10 shadow-2xl">
                <div className="absolute top-4 right-4">
                  <Smartphone className="w-8 h-8 text-yellow-400" />
                </div>
                <h3 className="text-2xl font-bold text-white mb-4">Abra sua conta agora!</h3>
                <ul className="space-y-3 mb-6">
                  <li className="flex items-center gap-2 text-gray-200">
                    <ChevronRight className="w-4 h-4 text-yellow-400" />
                    Sem taxas de abertura ou manutenção
                  </li>
                  <li className="flex items-center gap-2 text-gray-200">
                    <ChevronRight className="w-4 h-4 text-yellow-400" />
                    Cartão de crédito sem anuidade
                  </li>
                  <li className="flex items-center gap-2 text-gray-200">
                    <ChevronRight className="w-4 h-4 text-yellow-400" />
                    Rendimento automático na conta
                  </li>
                  <li className="flex items-center gap-2 text-gray-200">
                    <ChevronRight className="w-4 h-4 text-yellow-400" />
                    Aprovação em menos de 5 minutos
                  </li>
                </ul>
                <Button
                  variant="primary"
                  className="w-full bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold"
                  onClick={() => navigate('/register')}
                >
                  Começar Agora
                  <ArrowRight className="w-5 h-5 ml-2" />
                </Button>
              </div>
              <div className="absolute -bottom-4 -right-4 w-full h-full bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-3xl opacity-20 blur-xl" />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-4 bg-white/5 backdrop-blur-sm">
        <div className="container mx-auto max-w-6xl">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-white mb-4">
              O que nossos clientes dizem
            </h2>
            <p className="text-gray-200 text-lg">
              Confira a experiência de quem já faz parte do Digital Superbank
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {testimonials.map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                className="p-6 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-lg"
              >
                <div className="flex gap-1 mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <Star key={i} className="w-5 h-5 text-yellow-400 fill-yellow-400" />
                  ))}
                </div>
                <p className="text-gray-200 mb-6 italic">"{testimonial.comment}"</p>
                <div>
                  <div className="font-semibold text-white">{testimonial.name}</div>
                  <div className="text-sm text-gray-400">{testimonial.role}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Final */}
      <section className="py-20 px-4">
        <div className="container mx-auto max-w-4xl">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="bg-gradient-to-r from-yellow-500 to-yellow-600 rounded-3xl p-12 text-center relative overflow-hidden"
          >
            <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGRlZnM+PHBhdHRlcm4gaWQ9ImdyaWQiIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgcGF0dGVyblVuaXRzPSJ1c2VyU3BhY2VPblVzZSI+PHBhdGggZD0iTSAxMCAwIEwgMCAwIDAgMTAiIGZpbGw9Im5vbmUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS1vcGFjaXR5PSIwLjEiIHN0cm9rZS13aWR0aD0iMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-20" />
            
            <div className="relative z-10">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Pronto para transformar suas finanças?
              </h2>
              <p className="text-gray-800 text-lg mb-8">
                Abra sua conta grátis em menos de 5 minutos e comece a aproveitar todos os
                benefícios agora mesmo!
              </p>
              <Button
                size="lg"
                variant="secondary"
                onClick={() => navigate('/register')}
                className="bg-white text-gray-900 hover:bg-gray-100 font-semibold"
              >
                Abrir Minha Conta Grátis
                <ArrowRight className="w-5 h-5 ml-2" />
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-white/10">
        <div className="container mx-auto">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="text-gray-400 text-sm">
              © 2025 Digital Superbank. Todos os direitos reservados.
            </div>
            <div className="flex items-center gap-6 text-sm text-gray-400">
              <a href="#" className="hover:text-white transition-colors">
                Termos de Uso
              </a>
              <a href="#" className="hover:text-white transition-colors">
                Privacidade
              </a>
              <a href="#" className="hover:text-white transition-colors">
                Segurança
              </a>
              <a href="#" className="hover:text-white transition-colors">
                Contato
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
