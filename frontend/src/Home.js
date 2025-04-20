import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaYoutube, FaFileUpload } from 'react-icons/fa';
import './App.css';
function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [youtubeUrl, setYoutubeUrl] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    setIsLoading(true); // Set loading to true when the request starts
  
    const formData = new FormData();
  
    if (file) {
      formData.append('file', file);
    }
    if (youtubeUrl) {
      formData.append('youtube_url', youtubeUrl);
    }
  
    formData.append('content_type', file ? file.type.split('/')[0] : 'video');
  
    try {
      const response = await fetch('http://127.0.0.1:5000/process-content', {
        method: 'POST',
        body: formData,
      });
  
      if (response.ok) {
        const data = await response.json();
        navigate('/summary', { state: { summary: data.summary, questions: data.questions } });
      } else {
        console.error('Error processing content:', response.statusText);
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false); // Set loading to false when the request completes or fails
    }
  };

    return (
      <main>
        <div className="content">
          <h1>Welcome to Ai.tutor</h1>
          <p>Your AI-powered learning assistant</p>
          <div className="input-section">
            <div className="input-group file-upload">
              <span className="icon"><FaFileUpload /></span>
              <input
                id="file-upload"
                type="file"
                accept="video/*,application/pdf,audio/*"
                onChange={handleFileChange}
                className="hidden-file-input"
              />
              <label htmlFor="file-upload" className="file-upload-btn">
                Choose File (Video, Audio, PDF)
              </label>
              {file && <p className="file-name">{file.name}</p>}
            </div>
            <div className="input-group youtube">
              <span className="icon"><FaYoutube /></span>
              <input
                id="youtube-url"
                type="text"
                placeholder="Enter YouTube URL"
                value={youtubeUrl}
                onChange={(e) => setYoutubeUrl(e.target.value)}
              />
            </div>
          </div>
          <button onClick={handleSubmit} className="submit-btn" disabled={isLoading}>
            {isLoading ? 'Processing...' : 'Summarize'}
          </button>
        </div>
    
        {/* Loading Screen */}
        {isLoading && (
          <div className="loading-screen">
            <div className="loading-spinner"></div>
            <p>Processing your request...</p>
          </div>
        )}
      </main>
    );
}

export default Home;