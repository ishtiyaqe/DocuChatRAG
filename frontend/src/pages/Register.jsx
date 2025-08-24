import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import clients from "../api/clients";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await clients.post("api/auth/register/", {
        username,
        password,
      });
      alert("Registration successful! Please log in.");
      navigate("/login");
    } catch (err) {
      alert("Registration failed");
    }
  };

  return (
    <div className="flex items-center justify-center h-screen bg-gray-50">
      <form onSubmit={handleRegister} className="bg-white p-6 shadow rounded w-80">
        <h2 className="text-2xl mb-4 text-center">Register</h2>
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
          Register
        </button>
      </form>
    </div>
  );
}

export default Register;
