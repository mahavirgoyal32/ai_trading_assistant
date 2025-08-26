import React, { useState } from "react";
import axios from "axios";

function App() {
  const [command, setCommand] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!command.trim()) return;

    setLoading(true);
    setError("");
    setResponse(null);

    try {
      const res = await axios.post("http://localhost:8000/trade", {
        command,
      });
      setResponse(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || "Server error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center p-6">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">
        AI Trading Assistant
      </h1>

      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md flex space-x-2 mb-6"
      >
        <input
          type="text"
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          placeholder='e.g. "Buy 10 shares of AAPL at $180 limit"'
          className="flex-1 border rounded-xl p-3 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-blue-600 text-white px-4 py-2 rounded-xl shadow hover:bg-blue-700 disabled:opacity-50"
        >
          {loading ? "Processing..." : "Submit"}
        </button>
      </form>

      {error && (
        <div className="text-red-600 font-medium mb-4">⚠️ {error}</div>
      )}

      {response && response.need_clarification && (
        <div className="bg-yellow-100 border border-yellow-300 p-4 rounded-xl w-full max-w-md">
          <p className="font-semibold text-yellow-800 mb-2">Need Clarification:</p>
          <p className="text-gray-700">{response.message}</p>
        </div>
      )}

      {response && response.parsed && (
        <div className="bg-green-100 border border-green-300 p-4 rounded-xl w-full max-w-md">
          <p className="font-semibold text-green-800 mb-2">✅ Trade Executed</p>
          <pre className="text-sm text-gray-800 overflow-x-auto">
            {JSON.stringify(response, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}

export default App;
