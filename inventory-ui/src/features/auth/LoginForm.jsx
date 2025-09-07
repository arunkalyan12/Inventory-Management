import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../../services/api.js";

export default function LoginForm() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const result = await login(email, password);
      console.log("Logged in:", result);
      navigate("/dashboard"); // or wherever you want after login
    } catch (err) {
      setError(err.response?.data?.detail || "Login failed");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-gray-800 p-8 rounded-2xl shadow-lg w-full max-w-sm"
    >
      <div className="text-center mb-6">
        <img src="/logo.png" alt="Logo" className="w-16 mx-auto mb-2" />
        <h2 className="text-2xl font-bold">Log In</h2>
        <p className="text-gray-400 text-sm">
          Don’t have an account?{" "}
          <button
            type="button"
            className="text-blue-500 hover:underline"
            onClick={() => navigate("/signup")}
          >
            Sign Up
          </button>
        </p>
      </div>

      <input
        type="email"
        placeholder="Email Address"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        className="w-full p-3 mb-4 rounded bg-gray-700 border border-gray-600 placeholder-gray-400 focus:outline-none focus:border-blue-500"
        required
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        className="w-full p-3 mb-6 rounded bg-gray-700 border border-gray-600 placeholder-gray-400 focus:outline-none focus:border-blue-500"
        required
      />

      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}

      <button
        type="submit"
        className="w-full bg-blue-600 p-3 rounded hover:bg-blue-700 font-bold"
      >
        LOGIN
      </button>
    </form>
  );
}
