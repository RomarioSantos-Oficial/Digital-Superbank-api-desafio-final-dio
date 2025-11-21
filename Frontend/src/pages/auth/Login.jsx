import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useForm } from 'react-hook-form';
import { useAuth } from '../../hooks/useAuth';
import Button from '../../components/common/Button';
import Input from '../../components/common/Input';
import { IoMail, IoLockClosed } from 'react-icons/io5';

const Login = () => {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const { login } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const onSubmit = async (data) => {
    setLoading(true);
    const result = await login(data);
    setLoading(false);

    if (result.success) {
      navigate('/dashboard');
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
            Bem-vindo de volta!
          </h1>
          <p className="text-text-secondary">
            Faça login para acessar sua conta
          </p>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <Input
            label="Email ou CPF"
            type="text"
            placeholder="seu@email.com"
            icon={<IoMail />}
            error={errors.username?.message}
            {...register('username', { required: 'Campo obrigatório' })}
          />

          <Input
            label="Senha"
            type="password"
            placeholder="••••••••"
            icon={<IoLockClosed />}
            error={errors.password?.message}
            {...register('password', { required: 'Campo obrigatório' })}
          />

          <Button type="submit" fullWidth loading={loading}>
            Entrar
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-text-secondary">
            Não tem uma conta?{' '}
            <Link to="/register" className="text-primary-blue font-medium hover:underline">
              Cadastre-se
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
