import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import Camera from './Camera.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
    <Camera />
  </StrictMode>,
)
