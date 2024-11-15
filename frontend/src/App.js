import React, { useState } from 'react';
import './App.css';
import { FaRegEdit, FaQuestionCircle, FaUser, FaArrowLeft, FaGlobe } from 'react-icons/fa'; // For icons

function App() {
  const [contentType, setContentType] = useState(null);
  const [file, setFile] = useState(null);
  const [youtubeUrl, setYoutubeUrl] = useState('');
  const [summary, setSummary] = useState('');
  const [questions, setQuestions] = useState([]);
  const [showQuiz, setShowQuiz] = useState(false); // State to control quiz visibility
  const [selectedLanguage, setSelectedLanguage] = useState(''); // For language selection

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();

    if (file) {
      formData.append("file", file);
    }
    if (youtubeUrl) {
      formData.append("youtube_url", youtubeUrl);
    }

    formData.append("content_type", file ? file.type.split('/')[0] : "video");

    try {
      const response = await fetch("http://127.0.0.1:5000/process-content", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        setSummary(data.summary);
        setQuestions(data.questions);
      } else {
        console.error("Error processing content:", response.statusText);
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const handleBackClick = () => {
    window.history.back(); // Simple back button functionality
  };

  const handleTakeQuiz = () => {
    setShowQuiz(true); // Show quiz when "Take a Quiz" is clicked
  };

  // Handle language selection
  const handleLanguageChange = (e) => {
    setSelectedLanguage(e.target.value); // Update selected language
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>Learn Buddy</h1>
        <div className="nav-bar">
          <button className="nav-btn">
            <FaUser /> Profile
          </button>
          <button className="nav-btn">
            <FaRegEdit /> Write Buddy
          </button>
          <button className="nav-btn">
            <FaArrowLeft onClick={handleBackClick} /> Back
          </button>
        </div>
      </header>
      <div className="main-content">
        <div className="tabs">
          {/* Language selection dropdown */}
          <select
            className="language-dropdown"
            value={selectedLanguage}
            onChange={handleLanguageChange}
          >
            <option value="">Choose Language</option>
            <option value="en">English</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
            {/* Add more languages as required */}
          </select>
        </div>

        <div className="content">
          {/* File Upload Section */}
          <div className="file-upload">
            <label htmlFor="file-upload" className="file-upload-btn">
              Choose File
            </label>
            <input
              id="file-upload"
              type="file"
              accept="video/*,application/pdf,image/*"
              onChange={handleFileChange}
              className="hidden-file-input"
            />
            {file && <p className="file-name">{file.name}</p>}
          </div>

          {/* YouTube URL Input */}
          <input
            type="text"
            placeholder="Enter YouTube URL"
            value={youtubeUrl}
            onChange={(e) => setYoutubeUrl(e.target.value)}
          />
          <button onClick={handleSubmit} className="submit-btn">
            Summarize
          </button>

          {/* Display Summary */}
          {summary && (
            <div className="summary-section">
              <h2>Summary</h2>
              <p>{summary}</p>
            </div>
          )}

          {/* Take Quiz Button */}
          {questions.length > 0 && (
            <button onClick={handleTakeQuiz} className="quiz-btn">
              Take a Quiz
            </button>
          )}

          {/* Display Questions Only When Take a Quiz Button is Clicked */}
          {showQuiz && questions.length > 0 && (
            <div className="questions-section">
              <h2>Generated Questions</h2>
              <ul>
                {questions.map((question, index) => (
                  <li key={index}>{question}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
