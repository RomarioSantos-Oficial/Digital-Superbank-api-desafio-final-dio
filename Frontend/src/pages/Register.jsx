import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../hooks/useAuth';
import Button from '../components/common/Button';
import Input from '../components/common/Input';
import { IoPerson, IoMail, IoLockClosed, IoCall, IoCalendar, IoCard } from 'react-icons/io5';

const Register = () => {
  const { register: registerForm, handleSubmit, formState: { errors }, watch, setValue } = useForm();
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const password = watch('password');

  // Formatar CPF
  const formatCPF = (value) => {
    const numbers = value.replace(/\D/g, '');
    if (numbers.length <= 11) {
      return numbers
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,2})$/, '$1-$2');
    }
    return value;
  };

  // Formatar Telefone
  const formatPhone = (value) => {
    const numbers = value.replace(/\D/g, '');
    if (numbers.length <= 11) {
      return numbers
        .replace(/(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{5})(\d)/, '$1-$2');
    }
    return value;
  };

  const onSubmit = async (data) => {
    setLoading(true);
    const result = await registerUser({
      full_name: data.full_name,
      email: data.email,
      cpf: data.cpf,
      birth_date: data.birth_date,
      phone: data.phone,
      password: data.password,
    });
    setLoading(false);

    if (result.success) {
      navigate('/login');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-blue-green p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-primary-blue rounded-2xl flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-2xl">DS</span>
          </div>
          <h1 className="text-3xl font-bold text-primary-black mb-2">
            Criar Conta
          </h1>
          <p className="text-text-secondary">
            Preencha seus dados para começar
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <Input
            label="Nome Completo"
            placeholder="João da Silva"
            icon={<IoPerson />}
            error={errors.full_name?.message}
            {...registerForm('full_name', { 
              required: 'Nome completo é obrigatório',
              minLength: { value: 3, message: 'Nome deve ter pelo menos 3 caracteres' }
            })}
          />

          <Input
            label="Email"
            type="email"
            placeholder="seu@email.com"
            icon={<IoMail />}
            error={errors.email?.message}
            {...registerForm('email', { 
              required: 'Email é obrigatório',
              pattern: {
                value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                message: 'Email inválido'
              }
            })}
          />

          <Input
            label="CPF"
            placeholder="000.000.000-00"
            icon={<IoCard />}
            error={errors.cpf?.message}
            {...registerForm('cpf', { 
              required: 'CPF é obrigatório',
              pattern: {
                value: /^\d{3}\.\d{3}\.\d{3}-\d{2}$/,
                message: 'CPF inválido. Use formato: 000.000.000-00'
              }
            })}
            onChange={(e) => {
              const formatted = formatCPF(e.target.value);
              setValue('cpf', formatted);
            }}
          />

          <Input
            label="Data de Nascimento"
            type="date"
            icon={<IoCalendar />}
            error={errors.birth_date?.message}
            {...registerForm('birth_date', { 
              required: 'Data de nascimento é obrigatória'
            })}
          />

          <Input
            label="Telefone"
            placeholder="(00) 00000-0000"
            icon={<IoCall />}
            error={errors.phone?.message}
            {...registerForm('phone', { 
              required: 'Telefone é obrigatório',
              pattern: {
                value: /^\(\d{2}\) \d{5}-\d{4}$/,
                message: 'Telefone inválido. Use formato: (00) 00000-0000'
              }
            })}
            onChange={(e) => {
              const formatted = formatPhone(e.target.value);
              setValue('phone', formatted);
            }}
          />

          <Input
            label="Senha"
            type="password"
            placeholder="••••••••"
            icon={<IoLockClosed />}
            error={errors.password?.message}
            {...registerForm('password', {
              required: 'Senha é obrigatória',
              minLength: { value: 8, message: 'Mínimo 8 caracteres' }
            })}
          />

          <Input
            label="Confirmar Senha"
            type="password"
            placeholder="••••••••"
            icon={<IoLockClosed />}
            error={errors.confirmPassword?.message}
            {...registerForm('confirmPassword', {
              required: 'Confirme sua senha',
              validate: value => value === password || 'As senhas não coincidem'
            })}
          />

          <Button type="submit" fullWidth loading={loading}>
            Cadastrar
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-text-secondary">
            Já tem uma conta?{' '}
            <Link to="/login" className="text-primary-blue font-medium hover:underline">
              Faça login
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Register;
