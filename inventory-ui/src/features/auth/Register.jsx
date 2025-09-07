import { useAuth } from "../../context/AuthContext";

export default function Register() {
  const { loginWithOAuth } = useAuth();

  return (
    <div className="bg-gray-800 p-8 rounded-2xl shadow-2xl w-full max-w-md mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>
      <div className="flex flex-col gap-4">
        <button
          onClick={() => loginWithOAuth("google")}
          className="bg-red-600 hover:bg-red-700 p-3 rounded font-semibold"
        >
          Register with Google
        </button>
        <button
          onClick={() => loginWithOAuth("github")}
          className="bg-gray-700 hover:bg-gray-600 p-3 rounded font-semibold"
        >
          Register with GitHub
        </button>
      </div>
    </div>
  );
}
