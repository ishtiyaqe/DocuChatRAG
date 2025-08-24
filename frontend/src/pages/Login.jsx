import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../contexts/AuthContext";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login } = useContext(AuthContext); // <-- use login from AuthContext

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      await login({ username, password }); // <-- this updates AuthContext
      navigate("/"); // redirect after login
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
