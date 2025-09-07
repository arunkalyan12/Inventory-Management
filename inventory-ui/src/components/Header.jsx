import { useNavigate } from "react-router-dom";
import { getInitials } from "../utils/getInitials";

export default function Header({ user }) {
  const navigate = useNavigate();
  return (
    <div className="flex items-center justify-between bg-gray-800 p-4 rounded-b-2xl shadow-md">
      <div className="flex items-center space-x-4">
        <img
          src="/logo.png"
          alt="Logo"
          className="w-10 h-10 cursor-pointer"
          onClick={() => navigate("/dashboard")}
        />
        <button className="px-4 py-1 bg-gray-700 rounded-full hover:bg-gray-600">
          Dashboard
        </button>
        <button className="px-4 py-1 bg-gray-700 rounded-full hover:bg-gray-600">
          Shopping List
        </button>
      </div>
      <div className="flex items-center space-x-4">
        <button className="hover:bg-gray-700 p-2 rounded-full">
          <i className="fas fa-search"></i>
        </button>
        <button className="hover:bg-gray-700 p-2 rounded-full">
          <i className="fas fa-bell"></i>
        </button>
        <div className="w-10 h-10 bg-gray-700 rounded-full flex items-center justify-center text-white font-bold cursor-pointer">
          {getInitials(user.name)}
        </div>
      </div>
    </div>
  );
}
