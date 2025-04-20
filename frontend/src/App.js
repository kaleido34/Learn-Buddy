<<<<<<< HEAD
import logo from './logo.svg';
=======
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import { FaRegEdit, FaQuestionCircle, FaUser, FaArrowLeft, FaGlobe } from 'react-icons/fa';
import Home from './Home';
import Summary from './Summary';
import Quiz from './Quiz';
>>>>>>> 8ec4d88a0d921c1454d9930a07474727d9204006
import './App.css';

function App() {
  return (
<<<<<<< HEAD
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
=======
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
>>>>>>> 8ec4d88a0d921c1454d9930a07474727d9204006
