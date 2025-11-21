import React from 'react';
import { motion } from 'framer-motion';

const Card = ({
  children,
  className = '',
  hover = false,
  padding = true,
  ...props
}) => {
  const classes = `
    card
    ${hover ? 'cursor-pointer' : ''}
    ${!padding ? 'p-0' : ''}
    ${className}
  `.trim();
  
  return (
    <motion.div
      className={classes}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      whileHover={hover ? { y: -4 } : {}}
      {...props}
    >
      {children}
    </motion.div>
  );
};

export default Card;
