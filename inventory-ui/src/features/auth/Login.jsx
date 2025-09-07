import { useContext } from "react";
import { AuthContext } from "../../context/AuthContext";

export default function Login() {
  const { login } = useContext(AuthContext);

  const handleGoogleLogin = async () => {
    // You can use a popup or redirect to Google OAuth URL
    // Then POST the code to your backend
    const code = "CODE_FROM_GOOGLE"; // replace with real flow
    const res = await fetch("http://localhost:4000/auth/google", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code }),
    });
    const data = await res.json();
    login(data.token, data.user);
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <button
        className="px-6 py-3 bg-blue-600 text-white rounded shadow"
        onClick={handleGoogleLogin}
      >
        Login with Google
      </button>
    </div>
  );
}
