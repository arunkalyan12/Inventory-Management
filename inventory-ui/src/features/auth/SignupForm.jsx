import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { signup } from "../../services/api.js";

export default function SignupForm() {
  const navigate = useNavigate();
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!fullName.trim()) {
      setError("Full name is required!");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match!");
      return;
    }
    try {
      const result = await signup(fullName, email, password);
      setMessage(result.message || "Signup successful!");
      setError("");
      // Optionally clear the form
      setFullName("");
      setEmail("");
      setPassword("");
      setConfirmPassword("");
      // Redirect to login after a short delay
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError(err.response?.data?.detail || "Signup failed");
      setMessage("");
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-gray-800 p-8 rounded-2xl shadow-lg w-full max-w-sm"
    >
      <div className="text-center mb-6">
        <img src="/logo.png" alt="Logo" className="w-16 mx-auto mb-2" />
        <h2 className="text-2xl font-bold">Sign Up</h2>
        <p className="text-gray-400 text-sm">
          Already have an account?{" "}
          <button
            type="button"
            className="text-blue-500 hover:underline"
            onClick={() => navigate("/login")}
          >
            Log In
          </button>
        </p>
      </div>

      <input
        type="text"
        placeholder="Full Name"
        value={fullName}
        onChange={(e) => setFullName(e.target.value)}
        className="w-full p-3 mb-4 rounded bg-gray-700 border border-gray-600 placeholder-gray-400 focus:outline-none focus:border-blue-500"
        required
      />

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
        className="w-full p-3 mb-4 rounded bg-gray-700 border border-gray-600 placeholder-gray-400 focus:outline-none focus:border-blue-500"
        required
      />

      <input
        type="password"
        placeholder="Confirm Password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        className="w-full p-3 mb-6 rounded bg-gray-700 border border-gray-600 placeholder-gray-400 focus:outline-none focus:border-blue-500"
        required
      />

      {error && <p className="text-red-500 text-sm mb-4">{error}</p>}
      {message && <p className="text-green-500 text-sm mb-4">{message}</p>}

      <button
        type="submit"
        className="w-full bg-blue-600 p-3 rounded hover:bg-blue-700 font-bold"
      >
        SIGN UP
      </button>
    </form>
  );
}
