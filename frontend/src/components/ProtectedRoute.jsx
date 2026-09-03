import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    // Redirect unauthenticated users to the login page
    return <Navigate to="/login" replace />;
  }

  // Support both <ProtectedRoute><Component /></ProtectedRoute> 
  // and React Router v6 nested <Route element={<ProtectedRoute />}>
  return children ? children : <Outlet />;
}