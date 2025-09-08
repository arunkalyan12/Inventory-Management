import { createContext, useState, useEffect } from "react";
import axios from "axios";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Save user after login
  const login = (token, userInfo) => {
    localStorage.setItem("jwt", token);
    setUser(userInfo);
  };

  // Clear user on logout
  const logout = () => {
    localStorage.removeItem("jwt");
    setUser(null);
  };

  // Check if user is already logged in when app loads
  useEffect(() => {
    const token = localStorage.getItem("jwt");

    if (token) {
      // Verify the token by calling the backend
      axios
        .get("/me", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        .then((response) => {
          setUser(response.data);
        })
        .catch((error) => {
          console.error("Token verification failed:", error);
          logout(); // Clear invalid token
        })
        .finally(() => {
          setLoading(false);
        });
    } else {
      setLoading(false);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
}
