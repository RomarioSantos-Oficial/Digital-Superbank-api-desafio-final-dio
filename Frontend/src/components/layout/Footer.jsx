import React from 'react';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-white border-t border-gray-200 mt-auto">
      <div className="px-4 py-6">
        <div className="text-center text-sm text-text-secondary">
          <p>© {currentYear} Digital Superbank. Todos os direitos reservados.</p>
          <p className="mt-1">
            Banco 737 | CNPJ: 00.000.000/0001-00
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
