import React, { useEffect, useState } from 'react';
import DashboardLayout from '../components/layout/DashboardLayout';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import QuickNav from '../components/common/QuickNav';
import CVVModal from '../components/cards/CVVModal';
import { useAuth } from '../hooks/useAuth';
import { useCards } from '../hooks/useCards';
import { formatCardNumber, formatCurrency } from '../utils/formatters';
import { IoCard, IoLockClosed, IoLockOpen, IoAdd } from 'react-icons/io5';
import { SiVisa, SiMastercard } from 'react-icons/si';
import { FaCcDiscover } from 'react-icons/fa';

const Cards = () => {
  const { user } = useAuth();
  const { cards, loadCards, requestCard, blockCard, unblockCard, loading } = useCards();
  const [requesting, setRequesting] = useState(false);
  const [showCVVModal, setShowCVVModal] = useState(false);
  const [newCardData, setNewCardData] = useState(null);

  useEffect(() => {
    if (user?.id) {
      loadCards(user.id);
    }
  }, [user]);

  const handleRequestCard = async () => {
    setRequesting(true);
    const result = await requestCard({ user_id: user.id });
    setRequesting(false);
    
    if (result.success) {
      // Mostra modal com CVV se retornado
      if (result.data?.cvv) {
        setNewCardData(result.data);
        setShowCVVModal(true);
      }
      loadCards(user.id);
    }
  };

  const handleBlockCard = async (cardId) => {
    await blockCard(cardId);
    loadCards(user.id);
  };

  const handleUnblockCard = async (cardId) => {
    await unblockCard(cardId);
    loadCards(user.id);
  };

  const getCardGradient = (cardType) => {
    const gradients = {
      basic: 'from-green-400 to-green-600',
      plus: 'from-blue-500 to-blue-700',
      premium: 'from-gray-800 to-black',
      virtual: 'from-purple-500 to-purple-700',
    };
    return gradients[cardType] || gradients.basic;
  };

  const getBrandIcon = (brand) => {
    const icons = {
      'Visa': <SiVisa className="w-12 h-12" />,
      'Mastercard': <SiMastercard className="w-12 h-12" />,
      'Elo': <FaCcDiscover className="w-12 h-12" />,
    };
    return icons[brand] || <IoCard className="w-12 h-12 opacity-50" />;
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <QuickNav />
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white">Meu Cartão</h1>
            <p className="text-sm text-gray-400 mt-1">Cartão de Débito e Crédito vinculado às suas contas</p>
          </div>
          <Button onClick={handleRequestCard} loading={requesting}>
            <IoAdd className="w-5 h-5" />
            Solicitar Cartão
          </Button>
        </div>

        {loading ? (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-blue mx-auto"></div>
          </div>
        ) : cards.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {cards.map((card) => (
              <Card key={card.id} className="overflow-hidden">
                <div className={`bg-gradient-to-br ${getCardGradient(card.card_type)} text-white p-6 rounded-xl mb-4`}>
                  <div className="flex items-center justify-between mb-8">
                    <div className="flex flex-col gap-2">
                      <span className="text-sm font-medium">Digital Superbank</span>
                      <span className="text-xs bg-white bg-opacity-20 px-2 py-1 rounded-full w-fit">
                        Débito/Crédito
                      </span>
                    </div>
                    <div className="opacity-80">
                      {getBrandIcon(card.card_brand)}
                    </div>
                  </div>

                  <div className="mb-6">
                    <p className="text-xl tracking-wider font-mono">
                      {formatCardNumber(card.card_number, true)}
                    </p>
                  </div>

                  <div className="flex items-end justify-between">
                    <div>
                      <p className="text-xs opacity-70 mb-1">Nome</p>
                      <p className="font-medium uppercase">{user?.full_name}</p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs opacity-70 mb-1">Validade</p>
                      <p className="font-medium">
                        {card.expiry_date ? new Date(card.expiry_date).toLocaleDateString('pt-BR', { month: '2-digit', year: '2-digit' }).replace(/\//g, '/') : '--/--'}
                      </p>
                    </div>
                  </div>
                </div>

                <div className="space-y-3">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-text-secondary">Limite Total</span>
                    <span className="font-semibold">{formatCurrency(card.credit_limit)}</span>
                  </div>

                  <div className="flex items-center justify-between text-sm">
                    <span className="text-text-secondary">Disponível</span>
                    <span className="font-semibold text-primary-green">
                      {formatCurrency(card.available_limit)}
                    </span>
                  </div>

                  <div className="flex gap-2 pt-4 border-t border-gray-200">
                    {card.status === 'active' ? (
                      <Button
                        variant="danger"
                        size="small"
                        fullWidth
                        onClick={() => handleBlockCard(card.id)}
                      >
                        <IoLockClosed className="w-4 h-4" />
                        Bloquear
                      </Button>
                    ) : (
                      <Button
                        variant="success"
                        size="small"
                        fullWidth
                        onClick={() => handleUnblockCard(card.id)}
                      >
                        <IoLockOpen className="w-4 h-4" />
                        Desbloquear
                      </Button>
                    )}

                    <Button variant="secondary" size="small" fullWidth>
                      Ver Fatura
                    </Button>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        ) : (
          <Card>
            <div className="text-center py-12">
              <IoCard className="w-16 h-16 text-text-secondary mx-auto mb-4 opacity-50" />
              <p className="text-white font-semibold mb-2">Você ainda não possui cartão</p>
              <p className="text-text-secondary text-sm mb-4">
                Solicite seu cartão de débito e crédito.
                <br />
                Cada usuário pode ter apenas 1 cartão.
              </p>
              <Button onClick={handleRequestCard} className="mt-4" loading={requesting}>
                Solicitar Meu Cartão
              </Button>
            </div>
          </Card>
        )}
      </div>

      {/* Modal CVV */}
      <CVVModal
        isOpen={showCVVModal}
        onClose={() => setShowCVVModal(false)}
        cvv={newCardData?.cvv}
        cardNumber={newCardData?.card_number}
      />
    </DashboardLayout>
  );
};

export default Cards;
