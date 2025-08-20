import React, { useState } from "react";
import axios from "axios";

function QuestionAnswer({ docId }) {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);

    try {
      const response = await axios.post("http://localhost:8000/api/ask/", {
        doc_id: docId,
        question: question,
      });
      setAnswer(response.data.answer);
    } catch (error) {
      console.error(error);
      alert("Failed to get answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 w-full max-w-2xl">
      <h2 className="text-xl font-semibold mb-4">Ask a Question</h2>
      <textarea
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Type your question here..."
        className="w-full border rounded-lg p-3 mb-4"
      />
      <button
        onClick={handleAsk}
        disabled={loading}
        className="bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 disabled:bg-gray-400"
      >
        {loading ? "Thinking..." : "Ask"}
      </button>

      {answer && (
        <div className="mt-6 p-4 bg-gray-100 rounded-lg">
          <h3 className="font-semibold mb-2">Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
}

export default QuestionAnswer;
