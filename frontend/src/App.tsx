import { useState } from "react";
import axios from "axios";
import "./App.css";
import Navbar from "./components/Navbar.tsx";
import ResultDashboard from "./components/ResultDashboard";

function App() {
  const [invention, setInvention] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const analyzePatent = async () => {
    if (!invention.trim()) {
      alert("Please enter your invention.");
      return;
    }

    try {
      setLoading(true);

      const response = await axios.post(
        "http://127.0.0.1:8000/analyze",
        {
          invention: invention,
        }
      );

      setResult(response.data.result);

    } catch (error) {
      console.error(error);
      alert("Patent analysis failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
     <Navbar />
    <div className="app">

      <div className="hero">

        <div className="hero-eyebrow">
          <span className="dot" />
          AI Patent Research Engine
        </div>

        <h1>
          A place to verify your <em>next patent</em>
        </h1>

        <p className="hero-sub">
          Describe your invention and PatentMind AI will search prior art,
          score its novelty, and draft a filing strategy in minutes.
        </p>

        <div className="filing-field">
          <div className="filing-field-label">
            <span>Invention Disclosure</span>
          </div>

          <textarea
            rows={8}
            placeholder="Describe your invention in detail..."
            value={invention}
            onChange={(e) => setInvention(e.target.value)}
          />

          <div className="filing-actions">
            <button
              onClick={analyzePatent}
              disabled={loading}
            >
              {loading && <span className="spinner" aria-hidden="true" />}
              {loading ? "Analyzing..." : "Analyze Invention"}
            </button>
          </div>
        </div>

      </div>

      <hr />

      {result && (
        <ResultDashboard result={result} />
      )}

    </div>
    </>
  );
}

export default App;
