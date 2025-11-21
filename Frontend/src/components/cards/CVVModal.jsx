import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { IoClose, IoWarning, IoCopy } from 'react-icons/io5';
import toast from 'react-hot-toast';

const CVVModal = ({ isOpen, onClose, cvv, cardNumber }) => {
  const handleCopy = () => {
    navigator.clipboard.writeText(cvv);
    toast.success('CVV copiado!');
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-50 z-50"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.9, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.9, y: 20 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4"
            onClick={onClose}
          >
            <div
              className="bg-gray-800 rounded-2xl shadow-2xl max-w-md w-full p-6"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white">Cartão Criado!</h2>
                <button
                  onClick={onClose}
                  className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
                >
                  <IoClose className="w-6 h-6 text-gray-400" />
                </button>
              </div>

              <div className="bg-yellow-500 bg-opacity-10 border border-yellow-500 rounded-lg p-4 mb-6">
                <div className="flex items-start gap-3">
                  <IoWarning className="w-6 h-6 text-yellow-500 flex-shrink-0 mt-1" />
                  <div>
                    <h3 className="font-semibold text-yellow-500 mb-2">
                      Atenção: Guarde o CVV com segurança!
                    </h3>
                    <p className="text-sm text-gray-300">
                      Este é o único momento em que o CVV será exibido.
                      Por segurança, ele não poderá ser recuperado depois.
                    </p>
                  </div>
                </div>
              </div>

              <div className="bg-gray-700 rounded-lg p-6 mb-6">
                <div className="text-center">
                  <p className="text-gray-400 text-sm mb-2">Cartão</p>
                  <p className="text-white font-mono text-lg mb-4">
                    {cardNumber?.replace(/(\d{4})(?=\d)/g, '$1 ') || '****'}
                  </p>
                  
                  <p className="text-gray-400 text-sm mb-2">Código de Segurança (CVV)</p>
                  <div className="flex items-center justify-center gap-3">
                    <motion.p
                      initial={{ scale: 0 }}
                      animate={{ scale: 1 }}
                      className="text-yellow-500 font-mono text-4xl font-bold"
                    >
                      {cvv}
                    </motion.p>
                    <button
                      onClick={handleCopy}
                      className="p-2 hover:bg-gray-600 rounded-lg transition-colors"
                      title="Copiar CVV"
                    >
                      <IoCopy className="w-5 h-5 text-gray-400" />
                    </button>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <button
                  onClick={onClose}
                  className="w-full bg-yellow-500 hover:bg-yellow-600 text-gray-900 font-semibold py-3 rounded-lg transition-colors"
                >
                  Entendi, guardei o CVV
                </button>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
};

export default CVVModal;
