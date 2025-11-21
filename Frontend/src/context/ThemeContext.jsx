import React, { createContext, useState, useEffect } from 'react';
import { STORAGE_KEYS } from '../utils/constants';
import { storage } from '../utils/helpers';

export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState('light');

  useEffect(() => {
    // Carregar tema do localStorage
    const storedTheme = storage.get(STORAGE_KEYS.THEME, 'light');
    setTheme(storedTheme);
    applyTheme(storedTheme);
  }, []);

  const applyTheme = (newTheme) => {
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  };

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    storage.set(STORAGE_KEYS.THEME, newTheme);
    applyTheme(newTheme);
  };

  const value = {
    theme,
    toggleTheme,
    isDark: theme === 'dark',
  };

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
};
