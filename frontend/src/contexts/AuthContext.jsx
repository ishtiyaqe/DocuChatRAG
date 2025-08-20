
import React, { createContext, useEffect, useState } from "react";
import { getCurrentUser, loginUser, logoutUser, registerUser } from "../services/authService";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // On app load, check if logged in
  useEffect(() => {
    async function checkUser() {
      try {
        const data = await getCurrentUser();
        setUser(data);
      } catch (err) {
        setUser(null);
      } finally {
        setLoading(false);
      }
    }
    checkUser();
  }, []);

  const login = async (credentials) => {
    const data = await loginUser(credentials);
    setUser(data.user);
  };

  const register = async (userData) => {
    const data = await registerUser(userData);
    setUser(data.user);
  };

  const logout = async () => {
    await logoutUser();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
