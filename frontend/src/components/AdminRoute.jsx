import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function AdminRoute({ children }) {
  const { isAuthenticated, role } = useAuth();

  if (!isAuthenticated) {
    // Redirect unauthenticated users to login
    return <Navigate to="/login" replace />;
  }

  if (role !== 'admin') {
    // Redirect authenticated non-admins to their default functional page (e.g., /ask)
    return <Navigate to="/ask" replace />;
  }

  // Render the protected admin content
  return children ? children : <Outlet />;
}