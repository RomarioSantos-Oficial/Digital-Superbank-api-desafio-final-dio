import React from 'react';
import { Link } from 'react-router-dom';
import Button from '../components/common/Button';

const NotFound = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-light-gray p-4">
      <div className="text-center">
        <h1 className="text-9xl font-bold text-primary-blue mb-4">404</h1>
        <h2 className="text-3xl font-bold text-primary-black mb-4">
          Página não encontrada
        </h2>
        <p className="text-text-secondary mb-8">
          A página que você está procurando não existe ou foi movida.
        </p>
        <Link to="/dashboard">
          <Button>Voltar ao Dashboard</Button>
        </Link>
      </div>
    </div>
  );
};

export default NotFound;
