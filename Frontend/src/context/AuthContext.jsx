import React, { createContext, useState, useEffect } from 'react';
import { STORAGE_KEYS } from '../utils/constants';
import { storage } from '../utils/helpers';
import * as authService from '../services/auth.service';
import toast from 'react-hot-toast';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Carregar dados do localStorage ao iniciar
    const storedToken = storage.get(STORAGE_KEYS.TOKEN);
    const storedUser = storage.get(STORAGE_KEYS.USER);

    if (storedToken && storedUser) {
      setToken(storedToken);
      setUser(storedUser);
    }

    setLoading(false);
  }, []);

  const login = async (credentials) => {
    try {
      const response = await authService.login(credentials);
      
      const { access_token, token_type } = response;
      
      // Salvar token temporariamente
      storage.set(STORAGE_KEYS.TOKEN, access_token);
      setToken(access_token);
      
      // Buscar dados do usuário autenticado
      const userData = await authService.getCurrentUser();
      
      // Salvar usuário
      storage.set(STORAGE_KEYS.USER, userData);
      setUser(userData);
      
      toast.success('Login realizado com sucesso!');
      return { success: true };
    } catch (error) {
      toast.error(error.message || 'Erro ao fazer login');
      return { success: false, error: error.message };
    }
  };

  const register = async (userData) => {
    try {
      const response = await authService.register(userData);
      
      toast.success('Cadastro realizado com sucesso! Faça login para continuar.');
      return { success: true, data: response };
    } catch (error) {
      toast.error(error.message || 'Erro ao fazer cadastro');
      return { success: false, error: error.message };
    }
  };

  const logout = () => {
    storage.remove(STORAGE_KEYS.TOKEN);
    storage.remove(STORAGE_KEYS.USER);
    
    setToken(null);
    setUser(null);
    
    toast.success('Logout realizado com sucesso!');
  };

  const updateUserData = async () => {
    try {
      const userData = await authService.getCurrentUser();
      
      storage.set(STORAGE_KEYS.USER, userData);
      setUser(userData);
      
      return { success: true, data: userData };
    } catch (error) {
      console.error('Error updating user data:', error);
      return { success: false, error: error.message };
    }
  };

  const updateProfile = async (userId, data) => {
    try {
      const response = await authService.updateUser(userId, data);
      
      await updateUserData();
      
      toast.success('Perfil atualizado com sucesso!');
      return { success: true, data: response };
    } catch (error) {
      toast.error(error.message || 'Erro ao atualizar perfil');
      return { success: false, error: error.message };
    }
  };

  const changePassword = async (userId, passwordData) => {
    try {
      await authService.changePassword(userId, passwordData);
      
      toast.success('Senha alterada com sucesso!');
      return { success: true };
    } catch (error) {
      toast.error(error.message || 'Erro ao alterar senha');
      return { success: false, error: error.message };
    }
  };

  const isAuthenticated = () => {
    return !!token && !!user;
  };

  const value = {
    user,
    token,
    loading,
    login,
    register,
    logout,
    updateUserData,
    updateProfile,
    changePassword,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};
