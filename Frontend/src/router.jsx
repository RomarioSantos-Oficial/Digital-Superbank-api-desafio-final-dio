import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './hooks/useAuth';

// Pages
import Landing from './pages/Landing';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Accounts from './pages/Accounts';
import Transactions from './pages/Transactions';
import Cards from './pages/Cards';
import Investments from './pages/Investments';
import TradingView from './pages/TradingView';
import TradingDashboard from './pages/TradingDashboard';
import PayBills from './pages/PayBills';
import Statement from './pages/Statement';
import Profile from './pages/Profile';
import NotFound from './pages/NotFound';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-blue"></div>
      </div>
    );
  }

  return isAuthenticated() ? children : <Navigate to="/login" replace />;
};

const Router = () => {
  return (
    <Routes>
      {/* Landing Page */}
      <Route path="/" element={<Landing />} />

      {/* Public Routes */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected Routes */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/accounts"
        element={
          <ProtectedRoute>
            <Accounts />
          </ProtectedRoute>
        }
      />
      <Route
        path="/transactions"
        element={
          <ProtectedRoute>
            <Transactions />
          </ProtectedRoute>
        }
      />
      <Route
        path="/cards"
        element={
          <ProtectedRoute>
            <Cards />
          </ProtectedRoute>
        }
      />
      <Route
        path="/investments"
        element={
          <ProtectedRoute>
            <Investments />
          </ProtectedRoute>
        }
      />
      <Route
        path="/trading/:assetId"
        element={
          <ProtectedRoute>
            <TradingView />
          </ProtectedRoute>
        }
      />
      <Route
        path="/trading-dashboard"
        element={
          <ProtectedRoute>
            <TradingDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/trading-dashboard/:assetId"
        element={
          <ProtectedRoute>
            <TradingDashboard />
          </ProtectedRoute>
        }
      />
      <Route
        path="/pay-bills"
        element={
          <ProtectedRoute>
            <PayBills />
          </ProtectedRoute>
        }
      />
      <Route
        path="/statement"
        element={
          <ProtectedRoute>
            <Statement />
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Profile />
          </ProtectedRoute>
        }
      />

      {/* 404 */}
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default Router;
