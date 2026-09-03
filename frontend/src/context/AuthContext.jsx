import React, { createContext, useState, useContext } from 'react';
import { login as apiLogin, signup as apiSignup, setApiToken } from '../api/client';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  // State holds: { token, userId, email, role, institutionId } or null
  const [user, setUser] = useState(null);

  const login = async (email, password) => {
    const response = await apiLogin(email, password);
    
    // Store user data in React state
    const userData = {
      token: response.access_token,
      userId: response.user_id,
      email: response.email,
      role: response.role,
      institutionId: response.institution_id,
    };
    
    setUser(userData);
    setApiToken(response.access_token); // Sync with API client

    return response;
  };

  const signup = async (userData) => {
    const response = await apiSignup(userData);
    
    // If the institution is verified immediately, log the user in
    if (response.access_token) {
      const newUser = {
        token: response.access_token,
        userId: response.user_id,
        email: response.email,
        role: response.role,
        institutionId: response.institution_id,
      };
      setUser(newUser);
      setApiToken(response.access_token);
    }
    
    // Return the response to the component so it can handle the "pending" state vs success
    return response; 
  };

  const logout = () => {
    setUser(null);
    setApiToken(null);
  };

  const value = {
    user,
    isAuthenticated: !!user,
    role: user?.role || null,
    login,
    signup,
    logout,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

// Custom hook for consuming the AuthContext easily in components
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}