import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="App">
      <header className="App-header">
        <h1>React アプリケーションへようこそ！</h1>
        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            カウント: {count}
          </button>
          <p>
            このボタンをクリックしてカウンターを増やしてみてください
          </p>
        </div>
        <p>
          <code>src/App.jsx</code> を編集して変更を確認してください
        </p>
        <div className="links">
          <a
            className="App-link"
            href="https://react.dev"
            target="_blank"
            rel="noopener noreferrer"
          >
            React を学ぶ
          </a>
          <a
            className="App-link"
            href="https://vitejs.dev"
            target="_blank"
            rel="noopener noreferrer"
          >
            Vite について
          </a>
        </div>
      </header>
    </div>
  )
}

export default App
