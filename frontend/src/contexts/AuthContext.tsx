import React, { createContext, useContext, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

interface AuthState {
  user: any | null;
  onboardingComplete: boolean;
  isLoading: boolean;
}

interface AuthContextType extends AuthState {
  login: (userData: any) => void;
  logout: () => Promise<void>;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<AuthState>({
    user: null,
    onboardingComplete: false,
    isLoading: true,
  });
  const navigate = useNavigate();

  const refreshUser = async () => {
    // Try once, on 401 retry after a short delay to handle OAuth redirect race where cookie
    // may not be attached immediately by the browser.
    const attempt = async () => {
      const res = await api.get('/auth/me');
      setState({
        user: res.data,
        onboardingComplete: Boolean(res.data.onboarding_complete),
        isLoading: false,
      });
    };

    try {
      await attempt();
    } catch (err: any) {
      const status = err?.response?.status;
      if (status === 401) {
        // brief backoff and retry once
        await new Promise((r) => setTimeout(r, 300));
        try {
          await attempt();
          return;
        } catch (err2) {
          // fall through to clear state below
        }
      }
      setState({ user: null, onboardingComplete: false, isLoading: false });
    }
  };

  useEffect(() => {
    refreshUser();
  }, []);

  const login = (userData: any) => {
    setState({
      user: userData,
      onboardingComplete: userData.onboarding_complete,
      isLoading: false,
    });
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
      setState({ user: null, onboardingComplete: false, isLoading: false });
      navigate('/signin');
    } catch (err) {
      console.error('Logout failed:', err);
    }
  };

  return (
    <AuthContext.Provider value={{ ...state, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
