import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import DashboardLayout from '../components/layout/DashboardLayout';
import Card from '../components/common/Card';
import Button from '../components/common/Button';
import Input from '../components/common/Input';
import { useAuth } from '../hooks/useAuth';
import { useAccounts } from '../hooks/useAccounts';
import { useCards } from '../hooks/useCards';
import { useForm } from 'react-hook-form';
import { formatCPF, formatPhone, formatCurrency, formatDate } from '../utils/formatters';
import { 
  IoMail, IoCall, IoWallet, IoCard, 
  IoLockClosed, IoBusiness, IoAdd, IoDocumentText, IoPerson, IoKey, IoTrash, IoCopy
} from 'react-icons/io5';
import toast from 'react-hot-toast';
import * as pixService from '../services/pix.service';

const Profile = () => {
  const navigate = useNavigate();
  const { user, updateProfile, changePassword } = useAuth();
  const { accounts, createAccount, loadAccounts } = useAccounts();
  const { cards, loadCards, requestCard } = useCards();
  const [showPasswordForm, setShowPasswordForm] = useState(false);
  const [showAccountForm, setShowAccountForm] = useState(false);
  const [showPixForm, setShowPixForm] = useState(false);
  const [pixKeys, setPixKeys] = useState([]);
  const [loadingPix, setLoadingPix] = useState(false);

  const { register: registerProfile, handleSubmit: handleSubmitProfile } = useForm({
    defaultValues: {
      full_name: user?.full_name || '',
      email: user?.email || '',
      phone: user?.phone || '',
    }
  });

  const { register: registerPassword, handleSubmit: handleSubmitPassword, reset: resetPassword } = useForm();
  const { register: registerAccount, handleSubmit: handleSubmitAccount, reset: resetAccount } = useForm();
  const { register: registerPix, handleSubmit: handleSubmitPix, reset: resetPix } = useForm();

  useEffect(() => {
    if (user?.id) {
      loadCards(user.id);
      loadPixKeys();
    }
  }, [user]);

  const loadPixKeys = async () => {
    try {
      setLoadingPix(true);
      const data = await pixService.listPixKeys();
      setPixKeys(data.keys || []);
    } catch (error) {
      console.error('Erro ao carregar chaves PIX:', error);
      setPixKeys([]);
    } finally {
      setLoadingPix(false);
    }
  };

  const onSubmitProfile = async (data) => {
    const result = await updateProfile(user.id, data);
    if (result.success) {
      toast.success('Perfil atualizado com sucesso!');
    }
  };

  const onSubmitPassword = async (data) => {
    if (data.new_password !== data.confirm_password) {
      toast.error('As senhas não coincidem');
      return;
    }

    const result = await changePassword(user.id, {
      old_password: data.old_password,
      new_password: data.new_password
    });

    if (result.success) {
      resetPassword();
      setShowPasswordForm(false);
    }
  };

  const onSubmitAccount = async (data) => {
    const result = await createAccount({
      account_type: data.account_type,
      initial_deposit: parseFloat(data.initial_deposit) || 0
    });

    if (result.success) {
      resetAccount();
      setShowAccountForm(false);
      loadAccounts();
    }
  };

  const onSubmitPix = async (data) => {
    try {
      setLoadingPix(true);
      
      let keyValue = data.key_value || '';
      
      // Se for chave aleatória, gera UUID
      if (data.key_type === 'RANDOM') {
        keyValue = crypto.randomUUID();
      }
      
      // Remove formatação para enviar ao backend
      if (data.key_type === 'CPF' || data.key_type === 'PHONE') {
        keyValue = keyValue.replace(/[^\d]/g, '');
      }

      await pixService.createPixKey({
        account_id: parseInt(data.account_id),
        key_type: data.key_type,
        key_value: keyValue
      });

      toast.success('Chave PIX cadastrada com sucesso!');
      resetPix();
      setShowPixForm(false);
      loadPixKeys();
    } catch (error) {
      toast.error(error.message || 'Erro ao criar chave PIX');
    } finally {
      setLoadingPix(false);
    }
  };

  const handleDeletePixKey = async (keyId) => {
    if (!window.confirm('Deseja realmente excluir esta chave PIX?')) {
      return;
    }

    try {
      setLoadingPix(true);
      await pixService.deletePixKey(keyId);
      toast.success('Chave PIX removida com sucesso!');
      loadPixKeys();
    } catch (error) {
      toast.error(error.message || 'Erro ao excluir chave PIX');
    } finally {
      setLoadingPix(false);
    }
  };

  const handleCopyPixKey = (keyValue) => {
    navigator.clipboard.writeText(keyValue);
    toast.success('Chave copiada!');
  };

  const formatPixKeyValue = (type, value) => {
    if (type === 'CPF') {
      return formatCPF(value);
    }
    if (type === 'PHONE') {
      return formatPhone(value);
    }
    return value;
  };

  return (
    <DashboardLayout>
      <div className="space-y-6 max-w-5xl mx-auto">
        <h1 className="text-3xl font-bold text-white">Meu Perfil</h1>

        {/* Dados Pessoais */}
        <div className="space-y-6">\n          <Card>
            <h2 className="text-xl font-bold text-white mb-6">
              Informações Pessoais
            </h2>

              <div className="flex items-center gap-4 mb-6 pb-6 border-b border-gray-700">
                <div className="w-20 h-20 bg-yellow-500 rounded-full flex items-center justify-center text-gray-900 text-3xl font-bold">
                  {user?.full_name?.charAt(0)}
                </div>
                <div>
                  <h3 className="font-bold text-lg text-white">{user?.full_name}</h3>
                  <p className="text-gray-400">{user?.email}</p>
                </div>
              </div>

              <form onSubmit={handleSubmitProfile(onSubmitProfile)} className="space-y-4">
                <Input
                  label="Nome Completo"
                  icon={<IoPerson />}
                  {...registerProfile('full_name')}
                />

                <Input
                  label="Email"
                  type="email"
                  icon={<IoMail />}
                  {...registerProfile('email')}
                />

                <Input
                  label="Telefone"
                  icon={<IoCall />}
                  {...registerProfile('phone')}
                />

                <div>
                  <label className="label">CPF</label>
                  <p className="input bg-gray-700 text-gray-400">{formatCPF(user?.cpf)}</p>
                  <p className="text-xs text-gray-500 mt-1">
                    O CPF não pode ser alterado
                  </p>
                </div>

                <div>
                  <label className="label">Data de Nascimento</label>
                  <p className="input bg-gray-700 text-gray-400">
                    {user?.birth_date ? formatDate(user.birth_date) : '-'}
                  </p>
                </div>

                <Button type="submit" fullWidth>
                  Salvar Alterações
                </Button>
              </form>
            </Card>

            <Card>
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-white">Segurança</h2>
                <Button
                  variant="secondary"
                  onClick={() => setShowPasswordForm(!showPasswordForm)}
                >
                  <IoLockClosed className="mr-2" />
                  Alterar Senha
                </Button>
              </div>

              {showPasswordForm && (
                <form onSubmit={handleSubmitPassword(onSubmitPassword)} className="space-y-4 mt-4">
                  <Input
                    label="Senha Atual"
                    type="password"
                    icon={<IoLockClosed />}
                    {...registerPassword('old_password', { required: true })}
                  />

                  <Input
                    label="Nova Senha"
                    type="password"
                    icon={<IoLockClosed />}
                    {...registerPassword('new_password', { required: true, minLength: 8 })}
                  />

                  <Input
                    label="Confirmar Nova Senha"
                    type="password"
                    icon={<IoLockClosed />}
                    {...registerPassword('confirm_password', { required: true })}
                  />

                  <div className="flex gap-4">
                    <Button type="submit" fullWidth>
                      Alterar Senha
                    </Button>
                    <Button
                      type="button"
                      variant="secondary"
                      fullWidth
                      onClick={() => {
                        setShowPasswordForm(false);
                        resetPassword();
                      }}
                    >
                      Cancelar
                    </Button>
                  </div>
                </form>
              )}
            </Card>
          </div>

        {/* Minhas Contas */}
        <div className="space-y-6">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-bold text-white">Minhas Contas Bancárias</h2>
            <Button onClick={() => setShowAccountForm(!showAccountForm)}>
              <IoAdd className="mr-2" />
              Nova Conta
            </Button>
          </div>

            {showAccountForm && (
              <Card>
                <h3 className="text-lg font-bold text-white mb-4">Criar Nova Conta</h3>
                <form onSubmit={handleSubmitAccount(onSubmitAccount)} className="space-y-4">
                  {accounts.length === 0 && (
                    <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-3 mb-4">
                      <p className="text-yellow-500 text-sm">
                        ℹ️ Sua primeira conta deve ser uma Conta Corrente
                      </p>
                    </div>
                  )}
                  
                  <div>
                    <label className="label">Tipo de Conta</label>
                    <select className="input" {...registerAccount('account_type', { required: true })}>
                      <option value="">Selecione...</option>
                      <option value="CORRENTE">Conta Corrente</option>
                      {accounts.length > 0 && (
                        <>
                          <option value="POUPANCA">Poupança</option>
                          <option value="SALARIO">Conta Salário</option>
                          <option value="UNIVERSITARIA">Conta Universitária</option>
                          <option value="INVESTIMENTO">Conta Investimento (18+)</option>
                          <option value="EMPRESARIAL">Conta Empresarial (21+)</option>
                          <option value="BLACK">Conta Black (18+)</option>
                        </>
                      )}
                    </select>
                  </div>

                  <Input
                    label="Depósito Inicial (opcional)"
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    icon={<IoWallet />}
                    {...registerAccount('initial_deposit')}
                  />

                  <div className="flex gap-4">
                    <Button type="submit" fullWidth>
                      Criar Conta
                    </Button>
                    <Button
                      type="button"
                      variant="secondary"
                      fullWidth
                      onClick={() => {
                        setShowAccountForm(false);
                        resetAccount();
                      }}
                    >
                      Cancelar
                    </Button>
                  </div>
                </form>
              </Card>
            )}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {accounts.map((account) => (
                <Card key={account.id}>
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <IoBusiness className="w-5 h-5 text-yellow-500" />
                        <h3 className="font-bold text-white">
                          {account.account_type === 'CORRENTE' && 'Conta Corrente'}
                          {account.account_type === 'POUPANCA' && 'Poupança'}
                          {account.account_type === 'SALARIO' && 'Conta Salário'}
                          {account.account_type === 'UNIVERSITARIA' && 'Conta Universitária'}
                          {account.account_type === 'INVESTIMENTO' && 'Conta Investimento'}
                          {account.account_type === 'EMPRESARIAL' && 'Conta Empresarial'}
                          {account.account_type === 'BLACK' && 'Conta Black'}
                        </h3>
                      </div>
                      <p className="text-sm text-gray-400 mb-1">
                        Conta: {account.account_number}
                      </p>
                      <p className="text-sm text-gray-400">
                        Status: <span className={account.is_active ? 'text-green-400' : 'text-red-400'}>
                          {account.is_active ? 'Ativa' : 'Inativa'}
                        </span>
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-sm text-gray-400 mb-1">Saldo</p>
                      <p className="text-2xl font-bold text-yellow-500">
                        {formatCurrency(account.balance)}
                      </p>
                    </div>
                  </div>
                  <div className="mt-4 pt-4 border-t border-gray-700">
                    <Button 
                      variant="secondary" 
                      size="small" 
                      fullWidth
                      onClick={() => navigate('/transactions', { state: { accountId: account.id } })}
                    >
                      <IoDocumentText className="w-4 h-4" />
                      Ver Extrato
                    </Button>
                  </div>
                </Card>
              ))}
            </div>

            {accounts.length === 0 && (
              <Card>
                <div className="text-center py-8">
                  <IoWallet className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                  <p className="text-gray-400">Você ainda não possui contas bancárias</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Clique em "Nova Conta" para criar sua primeira conta
                  </p>
                </div>
              </Card>
            )}
          </div>

        {/* Meus Cartões */}
        <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-white">Meus Cartões de Crédito</h2>
              <Button onClick={() => requestCard({ user_id: user.id })}>
                <IoAdd className="mr-2" />
                Solicitar Cartão
              </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {cards.map((card) => (
                <Card key={card.id}>
                  <div className="bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-lg p-6 text-gray-900">
                    <div className="flex justify-between items-start mb-8">
                      <IoCard className="w-12 h-12" />
                      <p className="text-sm font-medium">
                        {card.card_category || 'Cartão de Crédito'}
                      </p>
                    </div>
                    
                    <div className="mb-6">
                      <p className="text-sm opacity-80 mb-1">Número do Cartão</p>
                      <p className="text-xl font-mono tracking-wider">
                        •••• •••• •••• {card.card_number?.slice(-4)}
                      </p>
                    </div>

                    <div className="flex justify-between items-end">
                      <div>
                        <p className="text-xs opacity-80 mb-1">Titular</p>
                        <p className="text-sm font-medium">{card.card_holder_name || user?.full_name}</p>
                      </div>
                      <div className="text-right">
                        <p className="text-xs opacity-80 mb-1">Validade</p>
                        <p className="text-sm font-medium">
                          {card.expiry_date ? new Date(card.expiry_date).toLocaleDateString('pt-BR', { month: '2-digit', year: '2-digit' }) : '--/--'}
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="mt-4 space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">Limite Total:</span>
                      <span className="text-white font-medium">{formatCurrency(card.credit_limit || 0)}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">Limite Disponível:</span>
                      <span className="text-green-400 font-medium">{formatCurrency(card.available_limit || 0)}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">Fatura Atual:</span>
                      <span className="text-yellow-500 font-medium">{formatCurrency(card.current_bill_amount || 0)}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">Status:</span>
                      <span className={`font-medium ${card.status === 'ACTIVE' ? 'text-green-400' : 'text-red-400'}`}>
                        {card.status === 'ACTIVE' ? 'Ativo' : card.status === 'BLOCKED' ? 'Bloqueado' : 'Cancelado'}
                      </span>
                    </div>
                  </div>
                </Card>
              ))}
            </div>

            {cards.length === 0 && (
              <Card>
                <div className="text-center py-8">
                  <IoCard className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                  <p className="text-gray-400">Você ainda não possui cartão</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Clique em "Solicitar Cartão" para pedir seu cartão de débito/crédito.
                    <br />
                    Cada usuário pode ter apenas 1 cartão.
                  </p>
                </div>
              </Card>
            )}
          </div>

        {/* Chaves PIX */}
        <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-white">Minhas Chaves PIX</h2>
              <Button onClick={() => setShowPixForm(!showPixForm)}>
                <IoAdd className="mr-2" />
                Adicionar Chave PIX
              </Button>
            </div>

            {showPixForm && (
              <Card>
                <h3 className="text-lg font-bold text-white mb-4">Cadastrar Nova Chave PIX</h3>
                <form onSubmit={handleSubmitPix(onSubmitPix)} className="space-y-4">
                  <div>
                    <label className="label">Tipo de Chave</label>
                    <select className="input" {...registerPix('key_type', { required: true })}>
                      <option value="">Selecione...</option>
                      <option value="CPF">CPF</option>
                      <option value="EMAIL">E-mail</option>
                      <option value="PHONE">Telefone</option>
                      <option value="RANDOM">Chave Aleatória</option>
                    </select>
                  </div>

                  <div>
                    <label className="label">Conta</label>
                    <select className="input" {...registerPix('account_id', { required: true })}>
                      <option value="">Selecione...</option>
                      {accounts.map((acc) => (
                        <option key={acc.id} value={acc.id}>
                          {acc.account_number} - {formatCurrency(acc.balance)}
                        </option>
                      ))}
                    </select>
                  </div>

                  <Input
                    label="Valor da Chave"
                    placeholder="Digite o valor da chave (deixe vazio para chave aleatória)"
                    {...registerPix('key_value')}
                  />

                  <div className="flex gap-4">
                    <Button type="submit" fullWidth disabled={loadingPix}>
                      {loadingPix ? 'Cadastrando...' : 'Cadastrar Chave'}
                    </Button>
                    <Button
                      type="button"
                      variant="secondary"
                      fullWidth
                      onClick={() => {
                        setShowPixForm(false);
                        resetPix();
                      }}
                    >
                      Cancelar
                    </Button>
                  </div>
                </form>
              </Card>
            )}

            {loadingPix ? (
              <Card>
                <div className="text-center py-8">
                  <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-yellow-500 mx-auto mb-4"></div>
                  <p className="text-gray-400">Carregando chaves PIX...</p>
                </div>
              </Card>
            ) : pixKeys.length > 0 ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {pixKeys.map((key) => (
                  <Card key={key.id}>
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex items-center gap-3">
                        <div className="p-3 bg-yellow-500 bg-opacity-10 rounded-lg">
                          <IoKey className="w-6 h-6 text-yellow-500" />
                        </div>
                        <div>
                          <p className="text-xs text-gray-400 uppercase">{key.key_type}</p>
                          <p className="text-white font-medium break-all">
                            {formatPixKeyValue(key.key_type, key.key_value)}
                          </p>
                        </div>
                      </div>
                    </div>
                    
                    <div className="text-xs text-gray-400 mb-4">
                      Cadastrada em {new Date(key.created_at).toLocaleDateString('pt-BR')}
                    </div>

                    <div className="flex gap-2">
                      <Button
                        variant="secondary"
                        size="small"
                        fullWidth
                        onClick={() => handleCopyPixKey(key.key_value)}
                      >
                        <IoCopy className="mr-2" />
                        Copiar
                      </Button>
                      <Button
                        variant="danger"
                        size="small"
                        onClick={() => handleDeletePixKey(key.id)}
                      >
                        <IoTrash />
                      </Button>
                    </div>
                  </Card>
                ))}
              </div>
            ) : (
              <Card>
                <div className="text-center py-8">
                  <IoKey className="w-16 h-16 text-gray-600 mx-auto mb-4" />
                  <p className="text-gray-400">Nenhuma chave PIX cadastrada</p>
                  <p className="text-sm text-gray-500 mt-2">
                    Clique em "Adicionar Chave PIX" para cadastrar sua primeira chave
                  </p>
                </div>
              </Card>
            )}
          </div>
      </div>
    </DashboardLayout>
  );
};

export default Profile;
