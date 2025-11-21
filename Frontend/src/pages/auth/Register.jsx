import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../../hooks/useAuth';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import { IoPerson, IoMail, IoLockClosed, IoCall } from 'react-icons/io5';

const Register = () => {
  const { register: registerForm, handleSubmit, formState: { errors }, watch } = useForm();
  const { register: registerUser } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const password = watch('password');

  const onSubmit = async (data) => {
    setLoading(true);
    const result = await registerUser({
      name: data.name,
      email: data.email,
      cpf: data.cpf,
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
            placeholder="João Silva"
            icon={<IoPerson />}
            error={errors.name?.message}
            {...registerForm('name', { required: 'Nome é obrigatório' })}
          />

          <Input
            label="Email"
            type="email"
            placeholder="seu@email.com"
            icon={<IoMail />}
            error={errors.email?.message}
            {...registerForm('email', { required: 'Email é obrigatório' })}
          />

          <Input
            label="CPF"
            placeholder="000.000.000-00"
            error={errors.cpf?.message}
            {...registerForm('cpf', { required: 'CPF é obrigatório' })}
          />

          <Input
            label="Telefone"
            placeholder="(00) 00000-0000"
            icon={<IoCall />}
            error={errors.phone?.message}
            {...registerForm('phone', { required: 'Telefone é obrigatório' })}
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
