import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      // Try JWT login
      const res = await axios.post("http://localhost:8000/api/auth/jwt/login/", {
        username,
        password,
      });

      if (res.data.access) {
        localStorage.setItem("access_token", res.data.access);
        localStorage.setItem("refresh_token", res.data.refresh);
        navigate("/");
        return;
      }

      // If no JWT, fallback to session login
      await axios.post(
        "http://localhost:8000/api/auth/session-login/",
        { username, password },
        { withCredentials: true }
      );
      navigate("/");
    } catch (err) {
      alert("Invalid login");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-50">
      <form onSubmit={handleLogin} className="bg-white p-6 shadow rounded w-80">
        <h2 className="text-2xl mb-4 text-center">Login</h2>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="border p-2 w-full mb-3 rounded"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="border p-2 w-full mb-3 rounded"
        />
        <button
          type="submit"
          className="bg-indigo-600 text-white w-full py-2 rounded"
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;
