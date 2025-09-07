import axios from 'axios';

const API_BASE_URL = "http://localhost:8000/api"; // Adjust if backend is on another port

export const signup = async (email, password) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/signup`, { email, password });
        return response.data;
    } catch (error) {
        console.error("Signup error:", error.response?.data || error.message);
        throw error;
    }
};

export const login = async (email, password) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/login`, { email, password });
        return response.data;
    } catch (error) {
        console.error("Login error:", error.response?.data || error.message);
        throw error;
    }
};
