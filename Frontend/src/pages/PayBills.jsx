import React, { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import DashboardLayout from '../components/layout/DashboardLayout';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Input from '../components/common/Input';
import QuickNav from '../components/common/QuickNav';
import { useAccounts } from '../hooks/useAccounts';
import { formatCurrency } from '../utils/formatters';
import * as billService from '../services/bill.service';
import toast from 'react-hot-toast';
import { 
  IoWaterOutline, 
  IoFlashOutline, 
  IoPhonePortraitOutline,
  IoTvOutline,
  IoCardOutline,
  IoReceiptOutline,
  IoBarcode,
  IoCheckmarkCircle
} from 'react-icons/io5';

const PayBills = () => {
  const { accounts } = useAccounts();
  const [selectedBillType, setSelectedBillType] = useState(null);
  const [showPaymentModal, setShowPaymentModal] = useState(false);
  const [paymentHistory, setPaymentHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const { register, handleSubmit, reset, formState: { errors } } = useForm();

  const billTypes = [
    { 
      id: 'water', 
      name: 'Água', 
      icon: IoWaterOutline, 
      color: 'blue',
      companies: ['SABESP', 'CEDAE', 'COMPESA', 'SANEPAR']
    },
    { 
      id: 'electricity', 
      name: 'Luz', 
      icon: IoFlashOutline, 
      color: 'yellow',
      companies: ['ENEL', 'CPFL', 'CEMIG', 'ENERGISA', 'LIGHT']
    },
    { 
      id: 'phone', 
      name: 'Telefone', 
      icon: IoPhonePortraitOutline, 
      color: 'green',
      companies: ['VIVO', 'CLARO', 'TIM', 'OI']
    },
    { 
      id: 'internet', 
      name: 'Internet/TV', 
      icon: IoTvOutline, 
      color: 'purple',
      companies: ['NET', 'SKY', 'VIVO FIBRA', 'CLARO TV', 'OI FIBRA']
    },
    { 
      id: 'gas', 
      name: 'Gás', 
      icon: IoFlashOutline, 
      color: 'orange',
      companies: ['COMGÁS', 'NATURGY', 'ULTRAGAZ']
    },
    { 
      id: 'other', 
      name: 'Outros', 
      icon: IoReceiptOutline, 
      color: 'gray',
      companies: ['IPTU', 'Condomínio', 'Escola', 'Academia']
    }
  ];

  const corrente = accounts.find(acc => acc.account_type === 'CORRENTE');

  useEffect(() => {
    loadPaymentHistory();
  }, []);

  const loadPaymentHistory = async () => {
    try {
      const history = await billService.getBillPaymentHistory(corrente?.id, 10);
      setPaymentHistory(history);
    } catch (error) {
      console.error('Erro ao carregar histórico:', error);
    }
  };

  const handleBillTypeSelect = (billType) => {
    setSelectedBillType(billType);
    setShowPaymentModal(true);
  };

  const onSubmit = async (data) => {
    if (!corrente) {
      toast.error('Você precisa de uma Conta Corrente');
      return;
    }

    const amount = parseFloat(data.amount);
    
    if (amount <= 0) {
      toast.error('Valor inválido');
      return;
    }

    if (corrente.balance < amount) {
      toast.error(`Saldo insuficiente. Disponível: ${formatCurrency(corrente.balance)}`);
      return;
    }

    setLoading(true);
    const loadingToast = toast.loading('Processando pagamento...');
    
    try {
      await billService.payBill({
        account_id: corrente.id,
        bill_type: selectedBillType.id,
        company: data.company,
        barcode: data.barcode,
        amount: amount,
        description: data.description
      });

      toast.dismiss(loadingToast);
      toast.success(
        `Pagamento de ${formatCurrency(amount)} realizado com sucesso!`,
        { duration: 4000 }
      );
      
      setShowPaymentModal(false);
      setSelectedBillType(null);
      reset();
      
      // Atualiza histórico e saldo
      await loadPaymentHistory();
      window.location.reload(); // Recarrega para atualizar saldo
      
    } catch (error) {
      toast.dismiss(loadingToast);
      toast.error(error.response?.data?.detail || 'Erro ao processar pagamento');
    } finally {
      setLoading(false);
    }
  };

  const getColorClasses = (color) => {
    const colors = {
      blue: 'bg-blue-900 text-blue-300 hover:bg-blue-800',
      yellow: 'bg-yellow-900 text-yellow-300 hover:bg-yellow-800',
      green: 'bg-green-900 text-green-300 hover:bg-green-800',
      purple: 'bg-purple-900 text-purple-300 hover:bg-purple-800',
      orange: 'bg-orange-900 text-orange-300 hover:bg-orange-800',
      gray: 'bg-gray-700 text-gray-300 hover:bg-gray-600'
    };
    return colors[color] || colors.gray;
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <QuickNav />
        
        <div>
          <h1 className="text-3xl font-bold text-white">Pagamento de Contas</h1>
          <p className="text-gray-400 mt-2">
            Pague suas contas de água, luz, telefone e muito mais
          </p>
        </div>

        {/* Saldo Disponível */}
        {corrente && (
          <Card className="bg-gradient-to-br from-yellow-500 to-yellow-600">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-900 font-medium">Saldo Disponível</p>
                <p className="text-3xl font-bold mt-1 text-gray-900">
                  {formatCurrency(corrente.balance)}
                </p>
                <p className="text-xs text-gray-800 mt-1">Conta Corrente</p>
              </div>
              <IoCardOutline className="w-12 h-12 text-gray-900 opacity-30" />
            </div>
          </Card>
        )}

        {/* Tipos de Contas */}
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {billTypes.map((billType) => {
            const Icon = billType.icon;
            return (
              <button
                key={billType.id}
                onClick={() => handleBillTypeSelect(billType)}
                className={`${getColorClasses(billType.color)} p-6 rounded-xl transition-all hover:scale-105 flex flex-col items-center gap-3`}
              >
                <Icon className="w-12 h-12" />
                <span className="font-medium text-sm text-center">{billType.name}</span>
              </button>
            );
          })}
        </div>

        {/* Modal de Pagamento */}
        {showPaymentModal && selectedBillType && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-gray-800 rounded-xl max-w-md w-full p-6 space-y-4">
              <div className="flex items-center justify-between">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <selectedBillType.icon className="w-6 h-6" />
                  Pagar {selectedBillType.name}
                </h2>
                <button
                  onClick={() => {
                    setShowPaymentModal(false);
                    setSelectedBillType(null);
                    reset();
                  }}
                  className="text-gray-400 hover:text-white"
                >
                  ✕
                </button>
              </div>

              <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
                {/* Empresa */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Empresa
                  </label>
                  <select
                    {...register('company', { required: true })}
                    className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-yellow-500"
                  >
                    <option value="">Selecione a empresa</option>
                    {selectedBillType.companies.map((company) => (
                      <option key={company} value={company}>
                        {company}
                      </option>
                    ))}
                  </select>
                  {errors.company && (
                    <p className="text-red-400 text-sm mt-1">Selecione a empresa</p>
                  )}
                </div>

                {/* Código de Barras */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Código de Barras
                  </label>
                  <div className="relative">
                    <IoBarcode className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      placeholder="00000.00000 00000.000000 00000.000000 0 00000000000000"
                      {...register('barcode', { 
                        required: true,
                        minLength: 47
                      })}
                      className="w-full pl-10 pr-4 py-3 bg-gray-700 border border-gray-600 rounded-lg text-white focus:outline-none focus:border-yellow-500"
                    />
                  </div>
                  {errors.barcode && (
                    <p className="text-red-400 text-sm mt-1">Código de barras inválido</p>
                  )}
                </div>

                {/* Valor */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Valor
                  </label>
                  <Input
                    type="number"
                    step="0.01"
                    min="0.01"
                    placeholder="0.00"
                    {...register('amount', { required: true, min: 0.01 })}
                  />
                  {errors.amount && (
                    <p className="text-red-400 text-sm mt-1">Valor inválido</p>
                  )}
                </div>

                {/* Descrição */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Descrição (opcional)
                  </label>
                  <Input
                    type="text"
                    placeholder="Ex: Conta de luz - Outubro/2025"
                    {...register('description')}
                  />
                </div>

                {/* Botões */}
                <div className="flex gap-3 pt-4">
                  <Button
                    type="button"
                    variant="secondary"
                    fullWidth
                    disabled={loading}
                    onClick={() => {
                      setShowPaymentModal(false);
                      setSelectedBillType(null);
                      reset();
                    }}
                  >
                    Cancelar
                  </Button>
                  <Button type="submit" fullWidth disabled={loading}>
                    {loading ? 'Processando...' : 'Pagar Agora'}
                  </Button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* Últimos Pagamentos */}
        <div>
          <h2 className="text-xl font-bold text-white mb-4">Últimos Pagamentos</h2>
          {paymentHistory.length > 0 ? (
            <div className="space-y-3">
              {paymentHistory.map((payment) => (
                <Card key={payment.transaction_id}>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-green-900 rounded-full flex items-center justify-center">
                        <IoCheckmarkCircle className="w-6 h-6 text-green-300" />
                      </div>
                      <div>
                        <p className="font-medium text-white">{payment.description}</p>
                        <p className="text-xs text-gray-500">
                          {new Date(payment.paid_at).toLocaleDateString('pt-BR', {
                            day: '2-digit',
                            month: 'short',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })}
                        </p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className="font-bold text-red-400">
                        - {formatCurrency(payment.amount)}
                      </p>
                      <span className="text-xs text-green-400">{payment.status}</span>
                    </div>
                  </div>
                </Card>
              ))}
            </div>
          ) : (
            <Card>
              <div className="text-center py-12">
                <IoReceiptOutline className="w-16 h-16 text-gray-600 mx-auto mb-4 opacity-50" />
                <p className="text-gray-400">Nenhum pagamento realizado ainda</p>
                <p className="text-sm text-gray-500 mt-2">
                  Seus pagamentos aparecerão aqui
                </p>
              </div>
            </Card>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default PayBills;
