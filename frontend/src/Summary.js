import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './App.css';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faQuestionCircle,
  faLayerGroup,
  faHeadphones,
} from "@fortawesome/free-solid-svg-icons";

function Summary() {
  const location = useLocation();
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);

  if (!location.state) {
    return <div>No data available. Please go back and try again.</div>;
  }

  const { summary, questions } = location.state;

  const handleTakeQuiz = () => {
    setIsLoading(true); // Set loading to true

    // Simulate a delay (e.g., 2 seconds) before navigating
    setTimeout(() => {
      navigate('/quiz', { state: { questions } });
    }, 1000); // Adjust the delay as needed
  };

  return (
    <div className="summary">
      <div className="summary-section">
        <h2>Summary</h2>
        <p>{summary}</p>
      </div>
      <div className="mindmap-section">
        <h2>Mind Map</h2>
        <p>Mind map visualization coming soon!</p>
      </div>
      <div className="buttons-container">
        <button onClick={handleTakeQuiz} className="quiz-btn" disabled={isLoading}>
          <FontAwesomeIcon icon={faQuestionCircle} /> {/* Quiz Icon */}
          <span>Quiz</span>
        </button>
        <button onClick="" className="flashcards-btn">
          <FontAwesomeIcon icon={faLayerGroup} /> {/* Flashcards Icon */}
          <span>Flashcards</span>
        </button>
        <button onClick="" className="audio-btn">
          <FontAwesomeIcon icon={faHeadphones} /> {/* Audio Icon */}
          <span>Audio</span>
        </button>
      </div>

      {/* Loading Screen */}
      {isLoading && (
        <div className="loading-screen">
          <div className="loading-spinner"></div>
          <p>Loading quiz...</p>
        </div>
      )}
    </div>
  );
}

export default Summary;