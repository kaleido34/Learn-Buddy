import React from 'react';
import { useLocation } from 'react-router-dom';
import './App.css';

function Quiz() {
  
  const location = useLocation();

  if (!location.state) {
    return <div>No quiz data available. Please go back and try again.</div>;
  }

  const { questions } = location.state;

  return (
    <div className="quiz-section">
  <h2>Practise Questions</h2>
  <ul className="questions-list">
    {questions.map((question, index) => (
      <li key={index} className="question-item">
        {question} {/* Removed numbering */}
      </li>
    ))}
  </ul>
</div>
  );
}

export default Quiz;