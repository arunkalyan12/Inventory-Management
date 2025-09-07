import { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);

  // Save user after login
  const login = (token, userInfo) => {
    localStorage.setItem("jwt", token);
    setUser(userInfo);
  };

  const logout = () => {
    localStorage.removeItem("jwt");
    setUser(null);
  };

  useEffect(() => {
    const token = localStorage.getItem("jwt");
    if (token) {
      // optionally verify token or decode
      setUser({ token });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}
