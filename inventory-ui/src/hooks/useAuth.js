import { useState, useEffect } from "react";

export function useAuth() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    fetch("/api/me", { credentials: "include" }) // backend route to return user info
      .then(res => res.json())
      .then(setUser)
      .catch(() => setUser(null));
  }, []);

  return { user };
}