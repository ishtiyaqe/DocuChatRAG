// src/App.jsx
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import DocumentUpload from "./components/DocumentUpload";
import QuestionAnswer from "./components/QuestionAnswer";
import LoginPage from "./pages/Login";
import RegisterPage from "./pages/Register";
import { AuthProvider } from "./contexts/AuthContext";
import PrivateRoute from "./components/PrivateRoute";

function App() {
  const [docId, setDocId] = useState(null);

  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/"
            element={
              <PrivateRoute>
                <div className="min-h-screen bg-gray-50 flex flex-col items-center p-6">
                  <h1 className="text-3xl font-bold text-indigo-600 mb-6">
                    Document Q&A Assistant
                  </h1>
                  {!docId ? (
                    <DocumentUpload onUploadSuccess={(id) => setDocId(id)} />
                  ) : (
                    <QuestionAnswer docId={docId} />
                  )}
                </div>
              </PrivateRoute>
            }
          />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
