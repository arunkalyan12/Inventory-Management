const API_URL = import.meta.env.VITE_API_URL;

export const login = async (token) => {
  const res = await fetch(`${API_URL}/auth/google`, {
    method: "POST",
    credentials: "include",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token }),
  });
  return res.json();
};
