import React, { useState, useMemo, useEffect } from 'react';
import clipboardCopy from 'clipboard-copy';
import './App.css';

interface Emoji {
  emoji: string;
  name: string;
}

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [toast, setToast] = useState<string | null>(null);
  const [emojis, setEmojis] = useState<Emoji[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/emojis.json')
      .then(res => res.json())
      .then(data => {
        setEmojis(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load emojis:', err);
        setLoading(false);
      });
  }, []);

  const filteredEmojis = useMemo(() => {
    const term = searchTerm.toLowerCase();
    return emojis.filter(e => 
      e.name.toLowerCase().includes(term) || 
      e.emoji.toLowerCase().includes(term)
    );
  }, [searchTerm, emojis]);

  const handleEmojiClick = async (emoji: string) => {
    try {
      await clipboardCopy(emoji);
      setToast(`Copied ${emoji} to clipboard!`);
      setTimeout(() => setToast(null), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div className="App">
      <header>
        <h1>Emoji Picker 🎉</h1>
        <p className="subtitle">Tap any emoji to copy it to your clipboard</p>
      </header>

      <div className="search-container">
        <input
          type="text"
          className="search-bar"
          placeholder="Search emojis..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          autoFocus
        />
        {searchTerm && (
          <button
            className="clear-btn"
            onClick={() => setSearchTerm('')}
            title="Clear search"
          >
            ×
          </button>
        )}
      </div>

      {loading ? (
        <p className="loading">Loading emojis...</p>
      ) : (
        <>
          <p className="count">Showing {filteredEmojis.length} of {emojis.length} emojis</p>

          <div className="emoji-grid">
        {filteredEmojis.length > 0 ? (
          filteredEmojis.map((item, index) => (
            <div
              key={index}
              className="emoji-item"
              onClick={() => handleEmojiClick(item.emoji)}
              title={item.name}
            >
              <span className="emoji-char">{item.emoji}</span>
              {searchTerm && <span className="emoji-name">{item.name}</span>}
            </div>
          ))
        ) : (
          <div className="no-results">
            No emojis found for "{searchTerm}"
          </div>
        )}
          </div>
        </>
      )}

      {toast && <div className="toast">{toast}</div>}
    </div>
  );
}

export default App;
