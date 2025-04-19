import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { FaRegEdit, FaQuestionCircle, FaUser, FaArrowLeft, FaGlobe } from 'react-icons/fa';
import Home from './Home';
import Summary from './Summary';
import Quiz from './Quiz';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <header >
          <h1>Ai.Tutor</h1>
          <nav>
            <Link to="/" className="btn">
              <FaUser /> Profile
            </Link>
            <Link to="/" className="btn">
              <FaRegEdit /> Write
            </Link>
            <Link to="/" className="btn">
              <FaArrowLeft /> Back
            </Link>
            <select className="language-dropdown">
              <option value="en" selected>English</option>
              <option value="es">Spanish</option>
              <option value="fr">French</option>
              <option value="de">German</option>
            </select>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/summary" element={<Summary />} />
            <Route path="/quiz" element={<Quiz />} />
          </Routes>
        </main>
        <footer>
          <p>&copy; 2025 Senp.ai. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;