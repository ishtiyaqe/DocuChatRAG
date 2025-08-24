import React, { useState } from "react";
import clients from "../api/clients";

function QuestionAnswer({ docId }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;

    setLoading(true);
    try {
      const response = await clients.post(
        `api/ask/${docId}/`,
        { question },
        {
        withCredentials: true,
        }
      );
      setAnswer(response.data.answer); // response should have answer from backend
    } catch (err) {
      console.error(err);
      alert("Error getting answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 shadow-lg rounded w-96 mt-6">
      <h2 className="text-xl font-semibold mb-4">Ask a Question</h2>
      <input
        type="text"
        placeholder="Type your question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        className="border p-2 w-full mb-3 rounded"
      />
      <button
        onClick={handleAsk}
        disabled={loading}
        className="bg-indigo-600 text-white px-4 py-2 rounded w-full"
      >
        {loading ? "Loading..." : "Ask"}
      </button>

      {answer && (
        <div className="mt-4 p-3 border rounded bg-gray-50">
          <h3 className="font-semibold mb-2">AI Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default QuestionAnswer;
